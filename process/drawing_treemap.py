import matplotlib.pyplot as plt
import pandas as pd
import squarify
from sqlalchemy import func
from matplotlib import cm

from crawl import creating_connection
from crawl.defining_items import Topics


def draw():
    # 创建数据库会话
    session = creating_connection.create_with_orm()

    # 查询数据
    query_result = session.query(
        Topics.topic_category,
        func.count(Topics.topic_id),
        func.sum(Topics.number_of_clicks),
        func.sum(Topics.number_of_replies)
    ).group_by(Topics.topic_category).all()

    # 关闭会话
    session.close()

    # 转换为 Pandas DataFrame
    df = pd.DataFrame(query_result, columns=['category', 'topic_count', 'total_clicks', 'total_replies'])

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['axes.unicode_minus'] = False

    # 设置点击数阈值
    click_threshold = 10000

    # 筛选出点击数超过阈值的话题
    df_filtered = df[df['total_clicks'] > click_threshold]

    # 使用话题数量
    sizes = df_filtered['topic_count']
    labels = df_filtered.apply(lambda x: f"{x['category']} {x['topic_count']}", axis=1)

    # 根据大小生成颜色映射
    norm = plt.Normalize(min(sizes), max(sizes))
    colors = [cm.Reds(norm(size)) for size in sizes]

    # 绘制树形图
    plt.figure(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, alpha=0.8, color=colors)
    plt.axis('off')
    plt.title('V2EX 各类别话题数量树形图')
    plt.show()
