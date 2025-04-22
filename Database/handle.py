import mysql.connector
from fontTools.misc.cython import returns


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="food_ordering_db"
    )
def validate_user(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None

    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return False

def check_user_exists(username: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None

    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return False


def add_user(username :str , password :str ) -> bool :
    try :
        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"

        cursor.execute(sql, (username,password))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return False

def add_food (foodname : str , category : str , price : str )-> bool :
    try :
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO `food` (`id`,`name`, `category` ,`price `) VALUES (%s, %s)"
        cursor.execute(sql ,())
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return False
