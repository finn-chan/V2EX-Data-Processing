import mysql
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import defining_model_topics
import option
import settings

args = option.Parse()
config = settings.Read(args['config'])


def create():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=config['host_name'],
            user=config['user_name'],
            passwd=config['user_password'],
            database=config['database_name']
        )
        print('成功连接到 MySQL 数据库')
    except Error as e:
        print(f'连接错误 \'{e}\'')
        return None

    return connection


def create_with_orm():
    engine = create_engine(
        f'mysql+pymysql://{config["user_name"]}:{config["user_password"]}@{config["host_name"]}:3306/v2ex_data',
        echo=False)

    # 创建表（如果尚不存在）
    defining_model_topics.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()
