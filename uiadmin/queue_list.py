import customtkinter as ctk


from Database.handle import get_connection, approve_account


class Queue_list(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nhập tài khoản cần được duyệt!",
            textvariable=self.search_var
        )
        self.search_entry.pack(padx=10, pady=(10, 5), fill="x")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.Queue_items = []
        self.load_queue_items()

    def load_queue_items(self):
        try:
            self.cursor.execute("SELECT username, password, full_name, email, phone FROM queue")
            rows = self.cursor.fetchall()

            for row in rows:
                self.create_queue_item(row[0], row[1], row[2], row[3], row[4])
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def approve_account(username, password, full_name, email, phone):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Cập nhật trạng thái tài khoản trong cơ sở dữ liệu (ví dụ: chuyển từ 'queue' sang 'approved')
            cursor.execute("""
                UPDATE queue SET status = 'approved' WHERE username = ?
            """, (username,))
            conn.commit()

            print(f"Tài khoản {username} đã được duyệt!")

        except Exception as e:
            print("Lỗi khi duyệt tài khoản:", e)

    def create_queue_item(self, username, password, full_name, email, phone):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(pady=5, fill="x", padx=10)

        label = ctk.CTkLabel(
            frame,
            text=f"{username} - {password} - [{full_name}] - {email} - {phone}",
            font=("Arial", 14)
        )
        label.pack(padx=10, pady=10)

        add_button = ctk.CTkButton(
            frame,
            text="Duyệt tài khoản",
            command=lambda: self.approve_account_and_remove_item(username, password, full_name, email, phone, frame)
        )

        add_button.pack(pady=(0, 10))

        self.Queue_items.append({
            "widget": frame,
            "username": username,
            "password": password,
            "full_name": full_name,
            "email": email,
            "phone": phone
        })

    def approve_account_and_remove_item(self, username, password, full_name, email, phone, frame):
        # Duyệt tài khoản
        approve_account(username, password, full_name, email, phone)

        # Xóa tài khoản khỏi danh sách Queue_items
        self.Queue_items = [item for item in self.Queue_items if item["username"] != username]

        # Ẩn widget tương ứng
        frame.pack_forget()

        print(f"Tài khoản {username} đã được duyệt và không còn trong danh sách.")
    def on_search(self, event=None):
        keyword = self.search_var.get().lower()

        # Ẩn tất cả các item trong danh sách Queue_items
        for item in self.Queue_items:
            item["widget"].pack_forget()

        # Hiển thị lại các item khớp với từ khóa tìm kiếm
        for item in self.Queue_items:
            if keyword in item["username"].lower():
                item["widget"].pack(pady=5, fill="x", padx=10)
                print("Tìm kiếm được tài khoản:", item["username"])
