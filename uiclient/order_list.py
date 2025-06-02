import customtkinter as ctk
from tkinter import messagebox
from Database.handle import get_connection
from Handle_login_logout.user_session import get_current_user

class OrderList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user = get_current_user()
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        username = self.user.username

        # Hiển thị đơn hàng "pending delivery"
        ctk.CTkLabel(self, text="ĐƠN HÀNG CHỜ XÁC NHẬN", font=("Arial", 16, "bold"), text_color="#FFD600").pack(pady=(15, 5))
        self.pending_frame = ctk.CTkFrame(self, fg_color="#2B2D31")
        self.pending_frame.pack(fill="x", padx=10, pady=5)
        self.load_order_items(username, frame=self.pending_frame, status="pending delivery")

        # Hiển thị các đơn còn lại
        ctk.CTkLabel(self, text="ĐƠN HÀNG ĐÃ XÁC NHẬN/KHÁC", font=("Arial", 16, "bold"), text_color="#00E676").pack(pady=(20, 5))
        self.other_frame = ctk.CTkFrame(self, fg_color="#2B2D31")
        self.other_frame.pack(fill="x", padx=10, pady=5)
        self.load_order_items(username, frame=self.other_frame, status="other")

    def load_order_items(self, username, frame, status):
        try:
            if status == "pending delivery":
                self.cursor.execute(
                    "SELECT order_id, order_status, food_item, address, quantity FROM orders WHERE username = %s AND order_status = %s",
                    (username, 'pending delivery')
                )
            else:
                self.cursor.execute(
                    "SELECT order_id, order_status, food_item, address, quantity FROM orders WHERE username = %s AND order_status != %s",
                    (username, 'pending delivery')
                )
            rows = self.cursor.fetchall()
            for row in rows:
                self.create_order_item(row[0], row[1], row[2], row[3], row[4], parent_frame=frame)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải đơn hàng: {e}")

    def create_order_item(self, order_id, order_status, food_item, address, quantity, parent_frame):
        # Frame chính cho mỗi món
        item_frame = ctk.CTkFrame(parent_frame, corner_radius=10, fg_color="#35383E")
        item_frame.pack(pady=10, fill="x", padx=10)

        # Label hiển thị thông tin món
        label_text = f"{food_item} ({address})\nĐơn hàng: {order_id} | Trạng thái: {order_status}"
        label = ctk.CTkLabel(item_frame, text=label_text, font=("Arial", 14), justify="left", text_color="#FFFFFF")
        label.pack(padx=10, pady=10, side="left", fill="both", expand=True)

        # Frame cho số lượng và nút điều chỉnh
        qty_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        qty_frame.pack(side="right", padx=10, pady=10)

        # Hiển thị số lượng
        qty_var = ctk.StringVar(value=str(quantity))
        qty_label = ctk.CTkLabel(qty_frame, textvariable=qty_var, font=("Arial", 14, "bold"), text_color="#FFFFFF")
        qty_label.pack(side="left", padx=5)

        # Nút giảm số lượng
        def decrease_quantity():
            new_qty = max(1, int(qty_var.get()) - 1)
            qty_var.set(str(new_qty))
            self.update_quantity(order_id, new_qty)

        minus_btn = ctk.CTkButton(qty_frame, text="-", command=decrease_quantity, fg_color="#00A8FF",
                                 hover_color="#0077B6", width=30, height=30, corner_radius=5)
        minus_btn.pack(side="left", padx=2)

        # Nút tăng số lượng
        def increase_quantity():
            new_qty = int(qty_var.get()) + 1
            qty_var.set(str(new_qty))
            self.update_quantity(order_id, new_qty)

        plus_btn = ctk.CTkButton(qty_frame, text="+", command=increase_quantity, fg_color="#00A8FF",
                                hover_color="#0077B6", width=30, height=30, corner_radius=5)
        plus_btn.pack(side="left", padx=2)

    def update_quantity(self, order_id, quantity):
        try:
            self.cursor.execute(
                "UPDATE orders SET quantity = %s WHERE order_id = %s AND order_status = %s",
                (quantity, order_id, 'pending delivery')
            )
            self.conn.commit()
            messagebox.showinfo("Thành công", "Số lượng đã được cập nhật!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật số lượng: {e}")

    def open_edit_order_dialog(self, order_id):
        # Lấy thông tin đơn hàng hiện tại
        self.cursor.execute(
            "SELECT food_item, address, quantity FROM orders WHERE order_id = %s", (order_id,)
        )
        result = self.cursor.fetchone()
        if not result:
            messagebox.showerror("Lỗi", "Không tìm thấy đơn hàng để chỉnh sửa.")
            return
        food_item, address, quantity = result

        # Popup chỉnh sửa
        popup = ctk.CTkToplevel(self)
        popup.title("Chỉnh sửa đơn hàng")
        popup.geometry("400x300")
        popup.resizable(False, False)
        popup.configure(fg_color="#2B2D31")

        # Tiêu đề
        ctk.CTkLabel(popup, text=f"Chỉnh sửa đơn hàng #{order_id}", font=("Arial", 16, "bold"), text_color="#FFFFFF").pack(pady=(15, 10))

        # Nhập món ăn
        ctk.CTkLabel(popup, text="Món ăn:", font=("Arial", 12), text_color="#FFFFFF").pack(pady=(5, 2), anchor="w", padx=20)
        food_entry = ctk.CTkEntry(popup, font=("Arial", 12), corner_radius=8)
        food_entry.insert(0, food_item)
        food_entry.pack(pady=2, padx=20, fill="x")

        # Nhập địa chỉ
        ctk.CTkLabel(popup, text="Địa chỉ:", font=("Arial", 12), text_color="#FFFFFF").pack(pady=(10, 2), anchor="w", padx=20)
        address_entry = ctk.CTkEntry(popup, font=("Arial", 12), corner_radius=8)
        address_entry.insert(0, address)
        address_entry.pack(pady=2, padx=20, fill="x")

        # Frame chứa các nút
        button_frame = ctk.CTkFrame(popup, fg_color="transparent")
        button_frame.pack(pady=20, fill="x", padx=20)

        def save_edit():
            new_food = food_entry.get().strip()
            new_address = address_entry.get().strip()
            if not new_food or not new_address:
                messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin món ăn và địa chỉ!")
                return
            try:
                self.cursor.execute(
                    "UPDATE orders SET food_item = %s, address = %s WHERE order_id = %s AND order_status = %s",
                    (new_food, new_address, order_id, 'pending delivery')
                )
                self.conn.commit()
                messagebox.showinfo("Thành công", "Đơn hàng đã được cập nhật thành công!")
                popup.destroy()
                # Tải lại danh sách đơn hàng
                for widget in self.pending_frame.winfo_children():
                    widget.destroy()
                for widget in self.other_frame.winfo_children():
                    widget.destroy()
                self.load_order_items(self.user.username, frame=self.pending_frame, status="pending delivery")
                self.load_order_items(self.user.username, frame=self.other_frame, status="other")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật đơn hàng: {e}")

        # Nút lưu
        save_btn = ctk.CTkButton(
            button_frame,
            text="Lưu thay đổi",
            command=save_edit,
            fg_color="#00E676",
            text_color="#23272E",
            hover_color="#00CC66",
            font=("Arial", 12, "bold"),
            width=120
        )
        save_btn.pack(side="left", padx=5)

        # Nút hủy
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Hủy",
            command=popup.destroy,
            fg_color="#FF5555",
            text_color="#23272E",
            hover_color="#CC4444",
            font=("Arial", 12, "bold"),
            width=120
        )
        cancel_btn.pack(side="right", padx=5)