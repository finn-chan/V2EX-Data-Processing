import re

from bs4 import BeautifulSoup
from dateutil import parser

import getting_web_page
import option
import recording_topic
import settings


def convert_to_mysql_datetime(time_str):
    if time_str:
        dt_with_tz = parser.parse(time_str)
        dt_without_tz = dt_with_tz.replace(tzinfo=None)
        return dt_without_tz.strftime('%Y-%m-%d %H:%M:%S')
    return None


def get(topic_id: str, cookie: str):
    page_url = f'https://v2ex.com/t/{topic_id}'
    page_content = getting_web_page.get(page_url, cookie)

    soup = BeautifulSoup(page_content, 'html.parser')

    # 楼主ID
    op_id = soup.find('div', class_='header').find('a')['href'].split('/')[-1]
    # 话题标题
    topic_header = soup.find('h1').text.strip()
    # 话题内容
    topic_content = soup.find('div', class_='topic_content').get_text(strip=True)
    # 提问时间
    question_time = soup.find('small', class_='gray').find('span').get('title')
    question_time = convert_to_mysql_datetime(question_time)
    # 点击数
    number_of_clicks = soup.find('small', class_='gray').contents[-1].strip().split(' ')[-2]

    # 检查是否有回复
    no_comments_yet = soup.find(id="no-comments-yet")
    if no_comments_yet:
        # 没有回复时，设置回复数为0，最后回复时间为空
        number_of_replies = '0'
        last_reply_time = None
    else:
        # 有回复时，提取回复数和最后回复时间
        number_of_replies = soup.find('span', class_='gray').text.split(' ')[0]
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

    # # 打印提取的信息
    # print(f'话题ID: {topic_id}')
    # print(f'楼主ID: {op_id}')
    # print(f'话题标题: {topic_header}')
    # print(f'话题内容: {topic_content}')
    # print(f'提问时间: {question_time}')
    # print(f'点击数: {number_of_clicks}')
    # print(f'回复数: {number_of_replies}')
    # print(f'最后回复时间: {last_reply_time}')
    # print(f'赞数: {up_vote_topic}')
    # print(f'踩数: {down_vote_topic}')
    # print(f'主题: {topic_category}')
    # for i, tag in enumerate(tags, 1):
    #     print(f'标签 {i}: {tag}')

    recording_topic.record(topic_id, op_id, topic_header, topic_content, question_time, number_of_clicks,
                           number_of_replies,
                           last_reply_time, up_vote_topic, down_vote_topic, topic_category, tags)

# args = option.Parse()
# config = settings.Read(args['config'])
# get(1000000, config['cookie'])
