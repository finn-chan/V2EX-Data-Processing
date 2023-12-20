# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class V2exProjectItem(scrapy.Item):
    topic_id = scrapy.Field()
    op_id = scrapy.Field()
    topic_header = scrapy.Field()
    topic_content = scrapy.Field()
    question_time = scrapy.Field()
    number_of_clicks = scrapy.Field()
    number_of_replies = scrapy.Field()
    last_reply_time = scrapy.Field()
    up_vote_topic = scrapy.Field()
    down_vote_topic = scrapy.Field()
    topic_category = scrapy.Field()
    tags = scrapy.Field()
