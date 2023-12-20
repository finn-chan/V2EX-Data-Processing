import re

from bs4 import BeautifulSoup
from dateutil import parser

import creating_connection
import getting_web_page
import option
import settings
from defining_items import Topics, Replies

args = option.Parse()
config = settings.Read(args['config'])


def convert_to_mysql_datetime(time_str: str):
    if time_str:
        dt_with_tz = parser.parse(time_str)
        dt_without_tz = dt_with_tz.replace(tzinfo=None)
        return dt_without_tz.strftime('%Y-%m-%d %H:%M:%S')
    return None


def get_question_info(soup: BeautifulSoup, topic_id: str, debug: int):
    # 楼主ID
    op_id = soup.find('div', class_='header').find('a')['href'].split('/')[-1]
    # 话题标题
    topic_header = soup.find('h1').text.strip()
    # 检查是否存在话题内容
    topic_content_div = soup.find('div', class_='topic_content')
    if topic_content_div:
        topic_content = topic_content_div.get_text(strip=True)
    else:
        topic_content = None
    # 提问时间
    question_time = soup.find('small', class_='gray').find('span').get('title')
    question_time = convert_to_mysql_datetime(question_time)
    # 点击数
    number_of_clicks = soup.find('small', class_='gray').contents[-1].strip().split(' ')[-2]

    # 检查是否存在回复
    no_comments_yet = soup.find(id='no-comments-yet')
    if no_comments_yet:
        # 没有回复时，设置回复数为0，最后回复时间为空
        number_of_replies = '0'
        last_reply_time = None
    else:
        # 存在回复时，提取回复数和最后回复时间
        number_of_replies = soup.find('span', class_='gray').text.split(' ')[0]
        # 如果回复数非数值，则赋值-1
        if not isinstance(number_of_replies, (int, float)):
            try:
                number_of_replies = int(number_of_replies)
            except ValueError:
                number_of_replies = -1
        last_reply_time = soup.find_all('span', class_='ago')[-1].get('title')
        last_reply_time = convert_to_mysql_datetime(last_reply_time)

    # 赞数和踩数，如果为空则设为零
    up_vote_topic = soup.find('div', id=re.compile('topic_.*_votes')).find_all('a')[0].get_text(strip=True)
    down_vote_topic = soup.find('div', id=re.compile('topic_.*_votes')).find_all('a')[1].get_text(strip=True)
    up_vote_topic = up_vote_topic if up_vote_topic.isdigit() else '0'
    down_vote_topic = down_vote_topic if down_vote_topic.isdigit() else '0'

    # 主题
    topic_category = soup.find('a', href=re.compile('/go/')).text.strip()
    # 标签1~4
    tags = soup.find_all('a', class_='tag')
    tags = [tag.get_text(strip=True) for tag in tags]

    if debug:
        # 打印提取的信息
        print(f'话题ID: {topic_id}')
        print(f'楼主ID: {op_id}')
        print(f'话题标题: {topic_header}')
        print(f'话题内容: {topic_content}')
        print(f'提问时间: {question_time}')
        print(f'点击数: {number_of_clicks}')
        print(f'回复数: {number_of_replies}')
        print(f'最后回复时间: {last_reply_time}')
        print(f'赞数: {up_vote_topic}')
        print(f'踩数: {down_vote_topic}')
        print(f'主题: {topic_category}')
        for i, tag in enumerate(tags, 1):
            print(f'标签 {i}: {tag}')

    # 方法一 传统的 SQL 模式提交
    # recording_topic.record(topic_id, op_id, topic_header, topic_content, question_time, number_of_clicks,
    #                        number_of_replies,
    #                        last_reply_time, up_vote_topic, down_vote_topic, topic_category, tags)

    # 方法二 使用 ORM 更新数据库
    session = creating_connection.create_with_orm()
    new_topic = Topics(
        topic_id=topic_id,
        op_id=op_id,
        topic_header=topic_header,
        topic_content=topic_content,
        question_time=question_time,
        number_of_clicks=number_of_clicks,
        number_of_replies=number_of_replies,
        last_reply_time=last_reply_time,
        up_vote_topic=up_vote_topic,
        down_vote_topic=down_vote_topic,
        topic_category=topic_category,
        tag_1=tags[0],
        tag_2=tags[1],
        tag_3=tags[2],
        tag_4=tags[3]
    )
    session.merge(new_topic)
    session.commit()

    return number_of_replies


def get_replies_info(soup: BeautifulSoup, topic_id: str, number_of_replies: int, debug: int):
    replies = []
    reply_cells = soup.find_all('div', class_='cell')
    floor_count = 0  # 初始化楼层数计数器

    # 创建数据库会话
    session = creating_connection.create_with_orm()

    for cell in reply_cells:
        # 检查是否为实际的回复单元
        if cell.find('strong') and cell.find('strong').find('a'):
            floor_count += 1  # 仅对实际的回复增加楼层数

            if floor_count > number_of_replies:
                break  # 如果达到指定的回复数量，则停止遍历

            # 回复者ID
            reply_user = cell.find('strong').find('a')['href'].split('/')[-1]
            # 回复内容
            reply_content = cell.find('div', class_='reply_content').get_text(strip=True)
            # 回复时间
            reply_time = cell.find('span', class_='ago').get('title')
            reply_time = convert_to_mysql_datetime(reply_time)
            # 感谢数
            number_of_thanks = cell.find('span', class_='small').get_text(strip=True) if cell.find('span',
                                                                                                   class_='small') else '0'
            # 是否楼主
            is_it_op = True if cell.find('div', class_='badge') else False

            # 创建回复对象
            new_reply = Replies(
                reply_id=reply_user,
                topic_id=topic_id,
                floor=floor_count,
                reply_content=reply_content,
                reply_time=reply_time,
                number_of_thanks=number_of_thanks,
                is_it_op=is_it_op
            )
            session.merge(new_reply)

            replies.append(new_reply)

    # 提交数据库会话
    session.commit()

    if debug:
        for reply in replies:
            print(
                f"回复者ID: {reply.reply_id}, 话题ID: {reply.topic_id}, 楼层: {reply.floor}, 回复内容: {reply.reply_content}, 回复时间: {reply.reply_time}, 感谢数: {reply.number_of_thanks}, 是否楼主: {reply.is_it_op}")

    # return replies



def get(topic_id: str, debug: int):
    page_url = f'https://v2ex.com/t/{topic_id}'
    page_content = getting_web_page.get(page_url, config['cookie'])

    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')

        # 获取提问者信息，返回回复数
        number_of_replies = get_question_info(soup, topic_id, debug)

        # 获取回复者信息
        get_replies_info(soup, topic_id, number_of_replies, debug)


# 调试
# get('1000000', 1)
