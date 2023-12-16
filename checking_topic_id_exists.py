import mysql.connector
from mysql.connector import MySQLConnection


def check(connection: MySQLConnection, topic_id: str):
    try:
        cursor = connection.cursor()
        query = 'SELECT EXISTS(SELECT 1 FROM topic WHERE topic_id = %s)'
        cursor.execute(query, (topic_id,))
        return cursor.fetchone()[0]
    except mysql.connector.Error as error:
        print(f'查询 topic_id 失败: {error}')
        return False
    finally:
        cursor.close()
