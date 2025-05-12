import customtkinter as ctk
from tkinter import messagebox
from Database.handle import get_connection

class Order_list(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, placeholder_text="nhập đơn hàng cần tìm", textvariable=self.search_var)
        self.search_entry.pack(padx=10, pady=(10, 5), fill="x")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.order_items = []
        self.load_order_items()

    def load_order_items(self):
        try:
            self.cursor.execute(
                "SELECT order_id, username, full_name, phone, address, food_item FROM orders WHERE order_status = %s",
                ('pending delivery',))

            for row in self.cursor.fetchall():
                self.create_order_items(*row)
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def create_order_items(self, order_id, username, full_name, phone, address, food_item):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(pady=5, fill="x", padx=10)

        info = f"{full_name} - {phone} - [{address}] - {food_item}"
        ctk.CTkLabel(frame, text=info, font=("Arial", 14)).pack(padx=10, pady=10)

        ctk.CTkButton(
            frame,
            text="✔️ Duyệt đơn hàng",
            command=lambda: self.approve_and_remove(order_id, frame)
        ).pack(pady=(0, 10))

        # Lưu thông tin của order bao gồm username
        self.order_items.append({"order_id": order_id, "username": username, "widget": frame})

    def approve_and_remove(self, order_id, frame):
        try:
            self.cursor.execute("UPDATE orders SET order_status = %s WHERE order_id = %s", ('delivered', order_id))
            self.conn.commit()
            frame.destroy()
            self.order_items = [item for item in self.order_items if item["order_id"] != order_id]
            messagebox.showinfo("Thành công", "Đơn hàng đã được duyệt")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không duyệt được đơn hàng: {e}")

    def on_search(self, event=None):
        keyword = self.search_var.get().lower()
        for item in self.order_items:
            item["widget"].pack_forget()
        for item in self.order_items:
            if keyword in item["username"].lower():
                item["widget"].pack(pady=5, fill="x", padx=10)
