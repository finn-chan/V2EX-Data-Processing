import pandas as pd
import plotly.express as px
from prettytable import PrettyTable
from sqlalchemy import func

from crawl import creating_connection
from crawl.defining_items import Topics, Replies


def draw():
    # 创建数据库会话
    session = creating_connection.create_with_orm()

    # 查询话题的回复数、点击数和感谢数
    query_result = session.query(
        Topics.topic_id,
        Topics.number_of_replies,
        Topics.number_of_clicks,
        func.coalesce(func.sum(Replies.number_of_thanks), 0).label('total_thanks')
    ).outerjoin(Replies, Topics.topic_id == Replies.topic_id) \
        .group_by(Topics.topic_id) \
        .order_by(Topics.number_of_replies.desc()) \
        .limit(100) \
        .all()

    # 关闭会话
    session.close()

    # 打印前10个话题的信息
    print('前10个活跃话题的信息')
    table = PrettyTable()
    table.field_names = ['话题ID', '回复数', '点击数', '感谢数']
    for item in query_result[:10]:
        table.add_row(item)
    print(table)

    # 转换为 Pandas DataFrame 用于绘制平行坐标图
    df = pd.DataFrame(query_result, columns=['topic_id', 'number_of_replies', 'number_of_clicks', 'number_of_thanks'])

    # 确保数据类型正确
    df['number_of_thanks'] = df['number_of_thanks'].astype(float)

    # 自定义颜色映射
    custom_color_scale = [
        [0, 'rgba(40, 100, 200, 0.8)'],  # 更鲜艳的蓝色
        [1, 'rgba(255, 10, 70, 0.8)']  # 柔和的红色
    ]

    # 绘制平行坐标图
    fig = px.parallel_coordinates(df, color='number_of_replies',
                                  dimensions=['number_of_replies', 'number_of_clicks', 'number_of_thanks'],
                                  labels={'number_of_replies': '回复数',
                                          'number_of_clicks': '点击数',
                                          'number_of_thanks': '感谢数'},
                                  title='V2EX 不同话题的多维特征展示',
                                  color_continuous_scale=custom_color_scale)
    fig.show()
