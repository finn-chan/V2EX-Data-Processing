import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from prettytable import PrettyTable
from sqlalchemy import func

from crawl import creating_connection
from crawl.defining_items import Topics, Replies


def draw():
    # 创建数据库会话
    session = creating_connection.create_with_orm()

    # 查询数据
    # 提问者的统计数据
    topics_stats = session.query(
        Topics.op_id,
        func.count(Topics.topic_id).label('post_count'),
        func.sum(Topics.number_of_replies).label('total_replies_received'),
        func.sum(Topics.up_vote_topic).label('total_up_votes')
    ).group_by(Topics.op_id).all()

    # 回复者的统计数据
    replies_stats = session.query(
        Replies.reply_id,
        func.count(Replies.reply_id).label('reply_count'),
        func.sum(Replies.number_of_thanks).label('total_thanks_received')
    ).group_by(Replies.reply_id).all()

    # 关闭会话
    session.close()

    # 转换为 Pandas DataFrame
    df_topics = pd.DataFrame(topics_stats)
    df_replies = pd.DataFrame(replies_stats)

    # 合并数据
    df = pd.merge(df_topics, df_replies, left_on='op_id', right_on='reply_id', how='outer').fillna(0)

    # 计算总活跃度：发帖数和回复数的总和
    df['total_activity'] = df['post_count'] + df['reply_count']

    # 选择基于总活跃度的前10个活跃用户进行展示
    top_active_users = df.nlargest(10, 'total_activity')

    # 打印前10位活跃用户的信息
    table = PrettyTable()
    table.field_names = ['用户ID', '发帖数', '收到回复数', '点赞数', '回复数', '感谢数']
    for idx, user in top_active_users.iterrows():
        user_id = user['op_id'] or user['reply_id']
        table.add_row(
            [user_id, user['post_count'], user['total_replies_received'], user['total_up_votes'], user['reply_count'],
             user['total_thanks_received']])

    print('前10位活跃用户的信息：')

    print(table)
    # 选择前5个活跃用户进行雷达图展示
    active_users = top_active_users.head(5)

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.rcParams['axes.unicode_minus'] = False

    # 绘制雷达图
    labels = np.array(['发帖数', '收到回复数', '点赞数', '回复数', '感谢数'])
    stats = active_users.loc[:,
            ['post_count', 'total_replies_received', 'total_up_votes', 'reply_count', 'total_thanks_received']].values

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    stats = np.concatenate((stats, stats[:, [0]]), axis=1)
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    # 绘制每个用户的数据并添加标签
    for idx, stat in enumerate(stats):
        user_id = active_users.iloc[idx]['op_id'] or active_users.iloc[idx]['reply_id']
        ax.plot(angles, stat, label=f'用户 ID: {user_id}')
        ax.fill(angles, stat, alpha=0.25)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title('V2EX 活跃用户表现')
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))  # 添加图例
    plt.show()
