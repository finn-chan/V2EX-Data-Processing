import jieba
import jieba.analyse
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

from crawl import creating_connection
from crawl.defining_items import Topics, Replies


def create():
    # 创建数据库会话
    session = creating_connection.create_with_orm()

    # 从 topics 表中提取数据
    topics_data = session.query(Topics.topic_header, Topics.topic_content).all()

    # 从 replies 表中提取数据
    replies_data = session.query(Replies.reply_content).all()

    # 关闭会话
    session.close()

    # 合并文本数据
    text_data = ' '.join([f'{topic[0]} {topic[1]}' for topic in topics_data] +
                         [reply[0] for reply in replies_data if reply[0]])

    # 提取中文关键词
    keywords = ' '.join(jieba.analyse.extract_tags(text_data, topK=100))

    # 合并中英文文本
    combined_text = text_data + ' ' + keywords

    # 添加中文停用词
    stopwords = set(STOPWORDS)
    stopwords.update(
        ['的', '了', '和', '是', '就', '都', '而', '及', '与', '着', '或', '一个', '没有', '我们', '你们', '他们',
         '它们', 'https'])

    # 加载 logo 图片作为蒙版
    logo_mask = np.array(Image.open('v2ex.png'))

    # 指定中文字体路径
    font_path = 'C:\Windows\Fonts\simsun.ttc'

    # 生成词云
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path, stopwords=stopwords,
                          mask=logo_mask, contour_width=1, contour_color='steelblue').generate(combined_text)

    # 显示词云
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('wordcloud.png', format='png')
    plt.show()
