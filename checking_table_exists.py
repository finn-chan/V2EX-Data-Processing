from mysql.connector import Error, MySQLConnection


def check(connection: MySQLConnection, table_name: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()
            return result is not None
    except Error as e:
        print(f"Error: {e}")
        return False
