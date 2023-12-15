import requests
from bs4 import BeautifulSoup

import stochastic_waiting


def get_web_page(url, cookie: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
        'Cookie': cookie
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 确保请求成功
        return response.text
    except requests.RequestException as e:
        print(f'请求错误: {e}')
        return None


def get(start_page: int, end_page: int, cookie: str):
    topic_ids = []

    for page in range(start_page, end_page + 1):
        page_url = f'https://v2ex.com/recent?p={page}'
        page_content = get_web_page(page_url, cookie)

        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            topic_links = soup.find_all('a', class_='topic-link')

            for link in topic_links:
                href = link.get('href')
                if href:
                    topic_id = href.split('/')[2].split('#')[0]
                    topic_ids.append(topic_id)

        stochastic_waiting.sleep()

    print(len(topic_ids))
    print(topic_ids)
