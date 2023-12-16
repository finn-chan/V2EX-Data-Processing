import mysql
from mysql.connector import Error

import option
import settings


def create():
    args = option.Parse()
    config = settings.Read(args['config'])

    connection = None
    try:
        connection = mysql.connector.connect(
            host=config['hostname'],
            user=config['user_name'],
            passwd=config['user_password'],
            database=config['database_name']
        )
        print("成功连接到 MySQL 数据库")
    except Error as e:
        print(f"连接错误 '{e}'")
        return None

    return connection
