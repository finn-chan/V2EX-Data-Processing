import requests
from bs4 import BeautifulSoup

import getting_topic_information
import getting_web_page
import stochastic_waiting


def get(start_page: int, end_page: int, cookie: str):
    topic_ids = []

    for page in range(start_page, end_page + 1):
        page_url = f'https://v2ex.com/recent?p={page}'
        page_content = getting_web_page.get(page_url, cookie)

        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            topic_links = soup.find_all('a', class_='topic-link')

            for link in topic_links:
                href = link.get('href')
                if href:
                    topic_id = href.split('/')[2].split('#')[0]
                    topic_ids.append(topic_id)

        print(f'即将获取第{page + 1}内容')
        stochastic_waiting.sleep()

    print(len(topic_ids))
    for topic_id in topic_ids:
        print(f'正在获取{topic_id}内容')
        getting_topic_information.get(topic_id, cookie)
        stochastic_waiting.sleep()
