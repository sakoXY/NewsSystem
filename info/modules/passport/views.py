from . import passport_blue
from ...utils.captcha.captcha import captcha


# 功能：获取图片验证码
@passport_blue.route('/image_code')
def image_code():
    # 调用generate_captcha获取图片验证码编号，验证码值，图片（二进制）
    name, text, image_data = captcha.generate_captcha()

    # 返回图片
    return image_data
