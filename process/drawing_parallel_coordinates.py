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

    # 使用 PrettyTable 输出前10个话题的信息
    table = PrettyTable()
    table.field_names = ['话题ID', '回复数', '点击数', '感谢数']
    for item in query_result[:10]:
        table.add_row(item)
    print(table)

    # 转换为 Pandas DataFrame 用于绘制平行坐标图
    df = pd.DataFrame(query_result, columns=['topic_id', 'number_of_replies', 'number_of_clicks', 'number_of_thanks'])

    # 检查数据
    print(df.head())

    # 确保数据类型正确
    df['number_of_thanks'] = df['number_of_thanks'].astype(float)

    # 绘制平行坐标图
    fig = px.parallel_coordinates(df, color='number_of_replies',
                                  dimensions=['number_of_replies', 'number_of_clicks', 'number_of_thanks'],
                                  labels={'number_of_replies': '回复数',
                                          'number_of_clicks': '点击数',
                                          'number_of_thanks': '感谢数'},
                                  title='不同话题的多维特征展示')
    fig.show()
