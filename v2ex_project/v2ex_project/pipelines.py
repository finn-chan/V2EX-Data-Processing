# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface

import creating_connection
from defining_items import Topics


class V2exProjectPipeline(object):

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(f"{data}\n")
        return item
        # spider.logger.info(f"Processing item: {item}")
        # new_topic = Topics(
        #     topic_id=item['topic_id'],
        #     op_id=item['op_id'],
        #     topic_header=item['topic_header'],
        #     topic_content=item['topic_content'],
        #     question_time=item['question_time'],
        #     number_of_clicks=item['number_of_clicks'],
        #     number_of_replies=item['number_of_replies'],
        #     last_reply_time=item['last_reply_time'],
        #     up_vote_topic=item['up_vote_topic'],
        #     down_vote_topic=item['down_vote_topic'],
        #     topic_category=item['topic_category'],
        #     tag_1=item['tags'][0] if len(item['tags']) > 0 else None,
        #     tag_2=item['tags'][1] if len(item['tags']) > 1 else None,
        #     tag_3=item['tags'][2] if len(item['tags']) > 2 else None,
        #     tag_4=item['tags'][3] if len(item['tags']) > 3 else None
        # )
        # self.session.merge(new_topic)
        # return item

    def open_spider(self, spider):
        self.file = open("123.json", 'w+')
        # # 在爬虫启动时创建数据库 session
        # self.session = creating_connection.create_with_orm()
        # spider.logger.info("Spider opened: Database session created")

    def close_spider(self, spider):
        self.file.close()
        # # 在爬虫关闭时提交 session 并关闭
        # self.session.commit()
        # self.session.close()
        # spider.logger.info("Spider closed: Database session committed and closed")
