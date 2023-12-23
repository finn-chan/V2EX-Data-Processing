import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.font_manager import FontProperties

from crawl import creating_connection
from crawl.defining_items import Topics, Replies


def draw():
    # 创建数据库会话
    session = creating_connection.create_with_orm()

    # 查询数据
    topics_query = session.query(Topics.question_time).all()
    replies_query = session.query(Replies.reply_time).all()

    # 关闭会话
    session.close()

    # 转换为 Pandas DataFrame
    df_topics = pd.DataFrame(topics_query, columns=['question_time'])
    df_replies = pd.DataFrame(replies_query, columns=['reply_time'])

    # 数据预处理
    df_topics['hour'] = pd.to_datetime(df_topics['question_time']).dt.hour
    df_replies['hour'] = pd.to_datetime(df_replies['reply_time']).dt.hour

    # 将小时逆序处理
    df_topics['hour'] = 23 - df_topics['hour']
    df_replies['hour'] = 23 - df_replies['hour']

    # 统计每小时的活跃度
    hourly_topics_count = df_topics.groupby('hour').size().reset_index(name='topic_count')
    hourly_replies_count = df_replies.groupby('hour').size().reset_index(name='reply_count')

    # 合并数据
    df = pd.merge(hourly_topics_count, hourly_replies_count, on='hour', how='outer').fillna(0)
    df['total_activity'] = df['topic_count'] + df['reply_count']

    # 设置中文字体
    font = FontProperties(fname=r'C:\Windows\Fonts\simsun.ttc', size=14)

    # 创建颜色映射
    cmap = LinearSegmentedColormap.from_list('activity_cmap', ['blue', 'red'])

    # 绘制热力图
    plt.figure(figsize=(12, 8))
    plt.scatter(y=df['hour'], x=df['total_activity'], s=df['total_activity'] * 3, c=df['total_activity'], cmap=cmap,
                alpha=0.6, edgecolors='w')
    cbar = plt.colorbar(label='活跃度')
    cbar.ax.set_ylabel('活跃度', fontproperties=font)
    plt.title('V2EX 每小时活跃度热力图', fontproperties=font)
    plt.ylabel('时间', fontproperties=font)
    plt.xlabel('活跃度', fontproperties=font)
    plt.yticks(range(24), [f'{23 - i:02d}:00' for i in range(24)])
    plt.grid(True)

    # 调整边界可视范围
    x_margin = 500
    y_margin = 2.5
    plt.xlim([df['total_activity'].min() - x_margin, df['total_activity'].max() + x_margin])
    plt.ylim([-y_margin, 24 + y_margin])

    plt.show()
