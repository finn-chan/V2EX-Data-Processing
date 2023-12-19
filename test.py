from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from v2ex_project.v2ex_project.spiders.v2ex_spider import V2exSpider


def run_spider(topic_id):
    # 获取项目设置
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    # 运行爬虫
    process.crawl(V2exSpider, topic_id=topic_id)
    process.start()


# 调用函数运行爬虫
run_spider('1001481')
