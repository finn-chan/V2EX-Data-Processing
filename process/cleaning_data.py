import re

from crawl import creating_connection
from crawl.defining_items import Topics, Replies


def clear_characters(text):
    # 保留字母、中文字符、中英文标点符号，去除 emoji 和其他特殊字符
    pattern = re.compile(
        u"([^\u4E00-\u9FA5\u0030-\u0039\u0041-\u005A\u0061-\u007A\u3000-\u303F\uff00-\uffef\u2010-\u201f\u0020-\u002f\u003a-\u0040\u005b-\u0060\u007b-\u007e])"
    )
    return pattern.sub(r'', text)


def clean():
    # 创建数据库会话
    session = creating_connection.create_with_orm()

    # 查询并删除 number_of_replies 为-1的行
    session.query(Topics).filter(Topics.number_of_replies == -1).delete()

    # # 更新Topics表
    # for topic in session.query(Topics).all():
    #     topic.topic_header = clear_characters(topic.topic_header)
    #     topic.topic_content = clear_characters(topic.topic_content)
    #
    # # 更新Replies表
    # for reply in session.query(Replies).all():
    #     reply.reply_content = clear_characters(reply.reply_content)

    # 提交更改
    session.commit()

    # 关闭会话
    session.close()
