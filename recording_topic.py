import mysql
import mysql.connector

import checking_topic_id_exists
import creating_connection
import creating_table_topic


def record(topic_id: str, op_id: str, topic_header: str, topic_content: str, question_time: str, number_of_clicks: str,
           number_of_replies: str,
           last_reply_time: str, up_vote_topic: str, down_vote_topic: str, topic_category: str, tags):
    # 连接到数据库
    connection = creating_connection.create()

    # 检查 topic 表是否存在
    creating_table_topic.create(connection)

    try:
        cursor = connection.cursor()

        if checking_topic_id_exists.check(connection, topic_id):
            # 准备 SQL 更新语句
            update_query = """
                UPDATE topics
                SET op_id = %s, topic_header = %s, topic_content = %s, question_time = %s, number_of_clicks = %s, number_of_replies = %s, last_reply_time = %s, up_vote_topic = %s, down_vote_topic = %s, topic_category = %s, tag_1 = %s, tag_2 = %s, tag_3 = %s, tag_4 = %s
                WHERE topic_id = %s
                """
            data = (
                op_id, topic_header, topic_content, question_time, number_of_clicks, number_of_replies,
                last_reply_time, up_vote_topic, down_vote_topic, topic_category, *tags[:4], topic_id
            )
            cursor.execute(update_query, data)
            print(f'topic {topic_id} 成功更新')
        else:
            # 准备 SQL 插入语句
            insert_query = """
                INSERT INTO topics (topic_id, op_id, topic_header, topic_content, question_time, number_of_clicks, number_of_replies, last_reply_time, up_vote_topic, down_vote_topic, topic_category, tag_1, tag_2, tag_3, tag_4)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            data = (
                topic_id, op_id, topic_header, topic_content, question_time, number_of_clicks, number_of_replies,
                last_reply_time, up_vote_topic, down_vote_topic, topic_category, *tags[:4]
            )
            cursor.execute(insert_query, data)
            print(f'topic {topic_id} 成功插入')

        # 提交事务
        connection.commit()

    except mysql.connector.Error as error:
        print(f'操作 MySQL 表记录失败: {error}')
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('MySQL 连接已关闭')
