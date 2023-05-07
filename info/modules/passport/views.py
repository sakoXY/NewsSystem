import json

from flask import request, current_app, make_response, jsonify

from . import passport_blue
from ... import redis_store, constants, db
from ...libs.yuntongxun.sms import CCP
from ...utils.captcha.captcha import captcha
import re
import random

from ...utils.response_code import RET


# 注册用户
# 请求路径: /passport/register
# 请求方式: POST
# 请求参数: mobile, sms_code,password
# 返回值: errno, errmsg
@passport_blue.route('/register', methods=['POST'])
def register():
    """
    1. 获取参数
    2. 校验参数,为空校验
    3. 手机号作为key取出redis中的短信验证码
    4. 判断短信验证码是否过期
    5. 判断短信验证码是否正确
    6. 删除短信验证码
    7. 创建用户对象
    8. 设置用户对象属性
    9. 保存用户到数据库
    10. 返回响应
    :return:
    """
    # 1. 获取参数
    # json_data = request.data
    # dict_data = json.loads(json_data)

    # 可以替换掉上面的两句话
    dict_data = request.json
    # dict_data = request.get_json()  # 等价于上面那句话

    mobile = dict_data.get("mobile")
    sms_code = dict_data.get("sms_code")
    password = dict_data.get("password")

    # 2. 校验参数,为空校验
    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全！")

    # 3. 手机号作为key取出redis中的短信验证码
    try:
        redis_sms_code = redis_store.get("sms_code:%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="短信验证码取出失败！")

    # 4. 判断短信验证码是否过期
    if not redis_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码已经过期！")

    # 5. 判断短信验证码是否正确
    if sms_code != redis_sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码填写错误！")

    # 6. 删除短信验证码
    try:
        redis_store.delete("sms_code:%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="短信验证码删除失败！")

    # 7. 创建用户对象
    from info.models import User
    user = User()

    # 8. 设置用户对象属性
    user.nick_name = mobile
    user.password_hash = password
    # user.password = password  # 密码的加密处理
    user.mobile = mobile
    user.signature = "该用户很懒,什么都没写"

    # 9. 保存用户到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="用户注册失败！")

    # 10. 返回响应
    return jsonify(errno=RET.OK, errmsg="注册成功！")


# 获取短信验证码
# 请求路径: /passport/sms_code
# 请求方式: POST
# 请求参数: mobile, image_code,image_code_id
# 返回值: errno, errmsg
@passport_blue.route('/sms_code', methods=['POST'])
def sms_code():
    """
    1. 获取参数
    2. 参数的为空校验
    3. 校验手机的格式
    4. 通过图片验证码编号获取,图片验证码
    5. 判断图片验证码是否过期
    6. 判断图片验证码是否正确
    7. 删除redis中的图片验证码
    8. 生成一个随机的短信验证码, 调用ccp发送短信,判断是否发送成功
    9. 将短信保存到redis中
    10. 返回响应
    :return:
    """
    # 1. 获取参数
    # json_data = request.data
    # dict_data = json.loads(json_data)
    dict_data = request.json # request.get_json()

    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")

    # 2. 参数的为空校验
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全！")

    # 3. 校验手机的格式
    if not re.match("1[3-9]\d{9}", mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号格式错误！")

    # 4. 通过图片验证码编号获取,图片验证码
    try:
        redis_image_code = redis_store.get("image_code:%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="操作redis失败！")

    # 5. 判断图片验证码是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码已经过期！")

    # 6. 判断图片验证码是否正确
    if image_code.upper() != redis_image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码填写错误！")

    # 7. 删除redis中的图片验证码
    try:
        redis_store.delete("image_code:%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="删除redis图片验证码失败！")

    # 8. 生成一个随机的短信验证码, 调用ccp发送短信,判断是否发送成功
    sms_code = "%06d" % random.randint(0, 999999)
    current_app.logger.debug("短信验证码是 = %s" % sms_code)
    # ccp = CCP()
    # result = ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES / 60], 1)
    #
    # if result == -1:
    #     return jsonify(errno=RET.DATAERR, errmsg="短信发送失败！")

    # 9. 将短信保存到redis中
    try:
        redis_store.set("sms_code:%s" % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="图片验证码保存到redis失败！")

    # 10. 返回响应
    return jsonify(errno=RET.OK, errmsg="短信发送成功！")


# 功能：获取图片验证码
# 请求路径：/passport/image_code
# 请求方法：get
# 携带参数：cur_id, pre_id
# 返回值：图片
@passport_blue.route('/image_code')
def image_code():
    # 1. 获取前端传递的参数
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")

    # 2. 调用generate_captcha获取图片验证码编号，验证码值，图片（二进制）
    name, text, image_data = captcha.generate_captcha()

    # 3. 将图片验证码的值保存redis
    try:
        # 参数1：key，参数2：value，参数3：有效期
        redis_store.set("image_code:%s" % cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

        # 判断是否有上一次的图片验证码
        if pre_id:
            redis_store.delete("image_code:%s" % pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return "图片验证码操作失败"

    # 4. 返回图片
    response = make_response(image_data)
    response.headers["Content-Type"] = "image/png"
    return response
