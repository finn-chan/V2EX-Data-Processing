import random

import scrapy
from dateutil import parser

import option
import settings

from v2ex_project.v2ex_project.items import V2exProjectItem

args = option.Parse()
config = settings.Read(args['config'])


def convert_to_mysql_datetime(datetime_str):
    try:
        dt = parser.parse(datetime_str)
        dt_naive = dt.replace(tzinfo=None)
        return dt_naive.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None


class V2exSpider(scrapy.Spider):
    name = 'v2ex'
    allowed_domains = ['v2ex.com']

    def __init__(self, topic_id=None, *args, **kwargs):
        super(V2exSpider, self).__init__(*args, **kwargs)
        self.topic_id = topic_id
        selected_domain = random.choice(self.allowed_domains)
        self.start_urls = [f'https://{selected_domain}/t/{self.topic_id}']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Cookie': config['cookie'],
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'TE': 'trailers'
        }

        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)

    def parse(self, response):

        # item = V2exProjectItem()

        # 话题ID
        topic_id = response.url.split('/')[-1]

        # 楼主ID
        op_id = response.css('div.header a::attr(href)').get().split('/')[-1]

        # 话题标题
        topic_header = response.css('h1::text').get().strip()

        # 话题内容
        topic_content_div = response.css('div.topic_content')
        topic_content = topic_content_div.css('::text').getall()
        topic_content = ' '.join(topic_content).strip() if topic_content else None

        # 提问时间
        question_time = response.css('small.gray span::attr(title)').get()
        question_time = convert_to_mysql_datetime(question_time) if question_time else None

        # 点击数
        clicks_and_replies = response.css('small.gray::text').getall()
        number_of_clicks = clicks_and_replies[-1].strip().split(' ')[-2] if clicks_and_replies else '0'

        # 回复数和最后回复时间
        no_comments_yet = response.css('#no-comments-yet')
        if no_comments_yet:
            number_of_replies = '0'
            last_reply_time = None
        else:
            replies_info = response.css('span.gray::text').get()
            number_of_replies = replies_info.split(' ')[0] if replies_info else '-1'
            last_reply_time = response.css('span.ago::attr(title)').getall()[-1]
            last_reply_time = convert_to_mysql_datetime(last_reply_time) if last_reply_time else None

        # 赞数和踩数
        votes = response.css('div[id^="topic_"] a::text').getall()
        up_vote_topic = votes[0] if votes and votes[0].isdigit() else '0'
        down_vote_topic = votes[1] if votes and len(votes) > 1 and votes[1].isdigit() else '0'

        # 主题
        topic_category = response.css('a[href^="/go/"]::text').get().strip()

        # 标签
        tags = response.css('a.tag::text').getall()

        # 构建数据字典
        topic_data = {
            'topic_id': topic_id,
            'op_id': op_id,
            'topic_header': topic_header,
            'topic_content': topic_content,
            'question_time': question_time,
            'number_of_clicks': number_of_clicks,
            'number_of_replies': number_of_replies,
            'last_reply_time': last_reply_time if last_reply_time else None,
            'up_vote_topic': up_vote_topic,
            'down_vote_topic': down_vote_topic,
            'topic_category': topic_category,
            'tags': tags if tags else []
        }

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

        yield topic_data
