import mysql
import mysql.connector

import creating_connection
import creating_topic_table


def record(topic_id: str, op_id: str, topic_header: str, topic_content: str, question_time: str, number_of_clicks: str,
           number_of_replies: str,
           last_reply_time: str, up_vote_topic: str, down_vote_topic: str, topic_category: str, tags):
    # 连接到数据库
    connection = creating_connection.create()

    # 检查 topic 表是否存在
    creating_topic_table.create(connection)

    try:
        cursor = connection.cursor()
        # 准备 SQL 插入语句
        insert_query = """
            INSERT INTO topic (topic_id, op_id, topic_header, topic_content, question_time, number_of_clicks, number_of_replies, last_reply_time, up_vote_topic, down_vote_topic, topic_category, tag_1, tag_2, tag_3, tag_4)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        # 准备要插入的数据
        data = (
            topic_id, op_id, topic_header, topic_content, question_time, number_of_clicks, number_of_replies,
            last_reply_time, up_vote_topic, down_vote_topic, topic_category, *tags[:4]
        )

        # 执行 SQL 语句
        cursor.execute(insert_query, data)
        connection.commit()
        print(f"topic {topic_id}成功插入")
    except mysql.connector.Error as error:
        print(f"插入 MySQL 表记录失败: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('MySQL 连接已关闭')
