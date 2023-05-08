from . import news_blue


@news_blue.route('/news_detail')
def news_detail():
    return "新闻详情展示"
