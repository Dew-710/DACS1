import customtkinter as ctk
from tkinter import messagebox
from Database.handle import get_connection

class Order_list(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        # Danh sách chờ xác minh
        ctk.CTkLabel(self, text="Đơn hàng CHƯA XÁC MINH (Đang xử lý)", font=("Arial", 16, "bold"), text_color="#FFD600").pack(pady=(15, 5))
        self.pending_frame = ctk.CTkFrame(self)
        self.pending_frame.pack(fill="x", padx=10)
        self.load_order_items(frame=self.pending_frame, status="Đang xử lý")

        # Danh sách đơn còn lại
        ctk.CTkLabel(self, text="Đơn hàng ĐÃ XÁC MINH/Khác", font=("Arial", 16, "bold"), text_color="#00E676").pack(pady=(18, 5))
        self.other_frame = ctk.CTkFrame(self)
        self.other_frame.pack(fill="x", padx=10)
        self.load_order_items(frame=self.other_frame, status="other")

    def load_order_items(self, frame, status):
        try:
            if status == "Đang xử lý":
                self.cursor.execute(
                    "SELECT order_id, username, full_name, phone, address, food_item, order_status FROM orders WHERE order_status = %s",
                    ('Đang xử lý',))
            else:
                self.cursor.execute(
                    "SELECT order_id, username, full_name, phone, address, food_item, order_status FROM orders WHERE order_status != %s",
                    ('Đang xử lý',))
            for row in self.cursor.fetchall():
                self.create_order_items(*row, parent_frame=frame)
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def create_order_items(self, order_id, username, full_name, phone, address, food_item, order_status, parent_frame):
        frame = ctk.CTkFrame(parent_frame, corner_radius=10)
        frame.pack(pady=5, fill="x", padx=10)

        info = f"{full_name} - {phone} - [{address}] - {food_item}\nTrạng thái: {order_status}"
        ctk.CTkLabel(frame, text=info, font=("Arial", 14)).pack(padx=10, pady=10)

        if order_status == "Đang xử lý":
            ctk.CTkButton(
                frame,
                text="✔️ Duyệt đơn hàng",
                command=lambda: self.approve_and_remove(order_id, frame)
            ).pack(pady=(0, 10))

    def approve_and_remove(self, order_id, frame):
        try:
            self.cursor.execute("UPDATE orders SET order_status = %s WHERE order_id = %s", ('Đã giao', order_id))
            self.conn.commit()
            frame.destroy()
            messagebox.showinfo("Thành công", "Đơn hàng đã được duyệt")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không duyệt được đơn hàng: {e}")
