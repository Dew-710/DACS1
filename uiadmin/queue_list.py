import customtkinter as ctk
from tkinter import messagebox
from Database.handle import get_connection

class Queue_list(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Nhập tài khoản cần được duyệt!", textvariable=self.search_var)
        self.search_entry.pack(padx=10, pady=(10, 5), fill="x")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.queue_items = []
        self.load_queue_items()

    def load_queue_items(self):
        try:
            self.cursor.execute("SELECT username, password, full_name, email, phone FROM users WHERE status = %s", ('inactive',))
            for row in self.cursor.fetchall():
                self.create_queue_item(*row)
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def create_queue_item(self, username, password, full_name, email, phone):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(pady=5, fill="x", padx=10)

        info = f"{username} - {password} - [{full_name}] - {email} - {phone}"
        ctk.CTkLabel(frame, text=info, font=("Arial", 14)).pack(padx=10, pady=10)

        ctk.CTkButton(
            frame,
            text="✔️ Duyệt tài khoản",
            command=lambda: self.approve_and_remove(username, frame)
        ).pack(pady=(0, 10))

        self.queue_items.append({"username": username, "widget": frame})

    def approve_and_remove(self, username, frame):
        try:
            self.cursor.execute("UPDATE users SET status = %s WHERE username = %s", ('active', username))
            self.conn.commit()
            frame.destroy()
            self.queue_items = [item for item in self.queue_items if item["username"] != username]
            messagebox.showinfo("Thành công", f"Đã duyệt tài khoản {username}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không duyệt được tài khoản: {e}")

    def on_search(self, event=None):
        keyword = self.search_var.get().lower()
        for item in self.queue_items:
            item["widget"].pack_forget()
        for item in self.queue_items:
            if keyword in item["username"].lower():
                item["widget"].pack(pady=5, fill="x", padx=10)
