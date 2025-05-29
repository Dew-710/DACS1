import mysql.connector
from Handle_login_logout.user import User





def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="100106",
        database="food_ordering_db"
    )
def validate_user(username: str, password: str):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT username, password, full_name, email, phone, address, role
            FROM users
            WHERE username = %s AND password = %s AND status = 'active'

        """
        cursor.execute(sql, (username, password))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return User(*result)
        else:
            return None
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return None

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


def add_user(username :str , password :str ,fullname :str,email :str ,phone :str,role :str, address : str) -> bool :
    try :
        conn = get_connection()
        cursor = conn.cursor()



        sql = "INSERT INTO `users` (`username`, `password`,`full_name`, `email`, `phone` , `role`,`address`) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql, (username,password,fullname,email,phone,role,address))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL : {e}")
        return False

def add_food(foodname: str, category: str, price: str) -> bool:
    try:
        price = float(price)

        conn = get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO `food` (`name`, `category`, `price`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (foodname, category, price))

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Lỗi khi thêm món ăn vào CSDL: {e}")
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

def Queue_add (username :str , password :str ,fullname :str,email :str ,phone :str ,address :str ,role : str, status : str) -> bool :
    try :
        conn = get_connection()
        cursor = conn.cursor()



        sql = "INSERT INTO `users` (`username`, `password`,`full_name`, `email`, `phone` , `role` , `address`, `status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql, (username,password,fullname,email,phone, role,address,  status))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL : {e}")
        return False



def approve_account(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username, password, full_name, email, phone, address, role FROM users WHERE username = %s", (username,))
        data = cursor.fetchone()

        if data and Queue_add(*data, status="active"):
            cursor.execute("UPDATE users SET status = 'active' WHERE username = %s", (username,))
            conn.commit()
            print(f"Duyệt tài khoản '{username}' thành công.")
        else:
            print(f"Lỗi duyệt tài khoản '{username}'.")
        cursor.close()
        conn.close()
    except Exception as e:
        print("Lỗi xử lý:", e)



def get_in4(username: str):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()


        if result is not None:
            return result
        else:
            return None
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return None
def delete_food(id: str):
    conn = get_connection()
    cursor = conn.cursor()
    try :
        sql= "DELETE FROM food WHERE id = %s"
        cursor.execute(sql,(id,))
        conn.commit()
    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return None


def update_user_info(username, password=None, email=None, phone=None, address=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()


        sql = "UPDATE users SET"
        params = []

        if password:
            sql += " password = %s,"
            params.append(password)
        if email:
            sql += " email = %s,"
            params.append(email)
        if phone:
            sql += " phone = %s,"
            params.append(phone)
        if address:
            sql += " address = %s,"
            params.append(address)

        sql = sql.rstrip(',')

        sql += " WHERE username = %s"
        params.append(username)

        cursor.execute(sql, tuple(params))

        conn.commit()

        print(f"[DB] Đã cập nhật thông tin người dùng với id {username}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Lỗi khi cập nhật thông tin người dùng: {e}")
def add_food_order(username, fullname, address, phone, order_status, food_items_str, total):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO `orders` (`username`, `full_name`, `address`, `phone`, `order_status`, `food_item`, `price`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (username, fullname, address, phone, order_status, food_items_str, total))
        conn.commit()

        order_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return order_id

    except Exception as e:
        print(f"Lỗi khi kết nối CSDL: {e}")
        return None
