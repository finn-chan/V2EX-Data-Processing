import mysql
from bs4 import BeautifulSoup

import option
import settings
from crawl import creating_connection
from crawl import getting_topic_information
from crawl import getting_web_page
from crawl import stochastic_waiting

args = option.Parse()
config = settings.Read(args['config'])


def remove_duplicates(topic_ids):
    # 连接到数据库
    connection = creating_connection.create()

    try:
        cursor = connection.cursor()
        # 创建一个集合来存储数据库中已存在的 topic_id
        existing_topic_ids = set()
        query = "SELECT topic_id FROM topic"
        cursor.execute(query)
        for (existing_id,) in cursor:
            existing_topic_ids.add(existing_id)

        # 移除已存在的 topic_id
        topic_ids = [id for id in topic_ids if int(id) not in existing_topic_ids]

    except mysql.connector.Error as error:
        print(f"数据库错误: {error}")
    finally:
        cursor.close()
        connection.close()
        print('MySQL 连接已关闭')

    return topic_ids


def get(start_page: int, end_page: int):
    topic_ids = []

    for page in range(start_page, end_page + 1):
        page_url = f'https://v2ex.com/recent?p={page}'
        page_content = getting_web_page.get(page_url, config['cookie'])

        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            topic_links = soup.find_all('a', class_='topic-link')

            for link in topic_links:
                href = link.get('href')
                if href:
                    topic_id = href.split('/')[2].split('#')[0]
                    topic_ids.append(topic_id)

        print(f'已获取第{page}页的内容')
        stochastic_waiting.sleep()

    # # 排除数据库中已存在的 topic
    # new_topic_ids = remove_duplicates(topic_ids)

    new_topic_ids = topic_ids
    print(f'获取了{len(new_topic_ids)}个 topics')

    for index, topic_id in enumerate(new_topic_ids, start=1):
        print(f'正在获取 topic:{topic_id} 内容 ({index}/{len(new_topic_ids)})')
        try:
            getting_topic_information.get(topic_id, 0)
        except Exception as e:
            print(f"处理 topic:{topic_id} 时发生错误: {e}")
        stochastic_waiting.sleep()
