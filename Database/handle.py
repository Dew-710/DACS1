import mysql.connector
from fontTools.misc.cython import returns


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="food_ordering_db"
    )
def validate_user(username: str, password: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        res="none"
        if result != None:
            print(result)
            res=result[5]
        return res
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return "none"

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


def add_user(username :str , password :str ,fullname :str,email :str ,phone :str,role :str) -> bool :
    try :
        conn = get_connection()
        cursor = conn.cursor()



        sql = "INSERT INTO `users` (`username`, `password`,`full_name`, `email`, `phone` , `role`) VALUES (%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql, (username,password,fullname,email,phone,role))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL : {e}")
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
def validate_foodname(keyword :str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM food WHERE name = %s"
        cursor.execute(sql, (keyword ,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result is not None

    except Exception as e:
        print(f"Lỗi khi kết nối CSDL mons awn : {e}")
        return False

def Queue_add (username :str , password :str ,fullname :str,email :str ,phone :str) -> bool :
    try :
        conn = get_connection()
        cursor = conn.cursor()



        sql = "INSERT INTO `queue` (`username`, `password`,`full_name`, `email`, `phone` ) VALUES (%s,%s,%s,%s,%s)"

        cursor.execute(sql, (username,password,fullname,email,phone))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL : {e}")
        return False


def approve_account( username, password, full_name, email, phone):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(

                "INSERT INTO queue (username, password, full_name, email, phone) VALUES (%s, %s, %s, %s, %s)",
                (username, password, full_name, email, phone)
            )
            cursor.execute("DELETE FROM queue WHERE username = %s", (username,))
            conn.commit()
            print(f"Tài khoản {username} đã được duyệt.")
        except Exception as e:
            print("Lỗi xử lý tài khoản:", e)