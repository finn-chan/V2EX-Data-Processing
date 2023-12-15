import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password, database_name):
    """创建数据库连接"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database_name
        )
        print("成功连接到 MySQL 数据库")
    except Error as e:
        print(f"连接错误 '{e}'")
        return None

    return connection


def create_table(connection, create_table_query):
    """在数据库中创建表"""
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print("表创建成功")
    except Error as e:
        print(f"创建表时出现错误 '{e}'")


def check(hostname: str, user_name: str, user_password: str, database_name: str):
    # 连接到数据库
    connection = create_connection(hostname, user_name, user_password, database_name)

    if connection is not None:
        # 创建表的SQL查询
        create_topic_table = """
        CREATE TABLE IF NOT EXISTS topic (
            topic_id INT PRIMARY KEY,
            op_id VARCHAR(20),
            topic_header TEXT,
            topic_content TEXT,
            question_time DATETIME,
            number_of_clicks INT,
            number_of_replies INT,
            last_reply_time DATETIME,
            up_vote_topic INT,
            down_vote_topic INT,
            topic_category VARCHAR(10),
            tag_1 VARCHAR(10),
            tag_2 VARCHAR(10),
            tag_3 VARCHAR(10),
            tag_4 VARCHAR(10)
        );
        """

        """
        topic_id        话题ID（主键）
        op_id        楼主ID
        topic_header        话题标题
        topic_content        话题内容
        question_time        提问时间
        number_of_clicks        点击数
        number_of_replies        回复数
        last_reply_time        最后回复时间
        up_vote_topic        赞数
        down_vote_topic        踩数
        topic_category        主题
        tag_1        标签1
        tag_2        标签2
        tag_3        标签3
        tag_4        标签4
        """

        # 创建表
        create_table(connection, create_topic_table)

        # 关闭数据库连接
        connection.close()
