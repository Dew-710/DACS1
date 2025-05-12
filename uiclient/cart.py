# uiclient/cart.py
import customtkinter as ctk
from customtkinter import CTkButton
from Handle_login_logout.user_session import get_current_user, set_current_user


class CartView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.cart_items = []
        self.cart_label = ctk.CTkLabel(self, text="Giỏ hàng", font=("Arial", 20))
        self.cart_label.pack(pady=10)

        self.cart_frame = ctk.CTkFrame(self)
        self.cart_frame.pack(pady=10)

        self.total_label = ctk.CTkLabel(self, text="Tổng cộng: 0 VNĐ", font=("Arial", 14))
        self.total_label.pack()
        submit_button = ctk.CTkButton(self, text="Đặt hàng", command=self.submit_order)
        submit_button.pack(pady=10)


    def add_item_to_cart(self, item_id, name, category, price):
        # Kiểm tra xem món đã có trong giỏ hàng chưa
        for item in self.cart_items:
            if item["id"] == item_id:
                item["quantity"] += 1
                break
        else:
            # Nếu chưa có, thêm mới với số lượng 1
            item = {
                "id": item_id,
                "name": name,
                "category": category,
                "price": price,
                "quantity": 1
            }
            self.cart_items.append(item)

        self.update_cart_view()

    def update_cart_view(self):
        # Xóa các widget cũ trong cart_frame
        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        total = 0

        for index, item in enumerate(self.cart_items):
            # Tính tiền món
            item_total = item["price"] * item["quantity"]
            total += item_total

            # Tạo dòng hiển thị: tên món, số lượng, giá, nút - +
            item_frame = ctk.CTkFrame(self.cart_frame)
            item_frame.pack(fill="x", pady=2)

            name_label = ctk.CTkLabel(item_frame, text=f"{item['name']} ({item['price']} VNĐ/món)", width=200,
                                                anchor="w")
            name_label.pack(side="left", padx=5)

            qty_label = ctk.CTkLabel(item_frame, text=f"Số lượng: {item['quantity']}", width=100)
            qty_label.pack(side="left")

            # Nút giảm
            minus_btn = ctk.CTkButton(item_frame, text="-", width=30,
                                                command=lambda i=index: self.change_quantity(i, -1))
            minus_btn.pack(side="left", padx=2)

            # Nút tăng
            plus_btn = ctk.CTkButton(item_frame, text="+", width=30,
                                               command=lambda i=index: self.change_quantity(i, 1))
            plus_btn.pack(side="left", padx=2)


        self.total_label.configure(text=f"Tổng cộng: {total} VNĐ")
        return total



    def change_quantity(self, index, delta):
        item = self.cart_items[index]
        item["quantity"] += delta

        if item["quantity"] <= 0:
            # Nếu số lượng <= 0 thì xoá món khỏi giỏ
            del self.cart_items[index]

        self.update_cart_view()

    def submit_order(self):
        self.user = get_current_user()

        username = self.user.username
        fullname = self.user.fullname
        address = self.user.address
        phone = self.user.phone
        order_status = "pending delivery"

        if not self.cart_items:
            print("Giỏ hàng trống!")
            return

        print(f"Người đặt hàng: {username}")
        print("Gửi đơn hàng:")

        # Chuỗi món ăn và số lượng
        food_items_str = ", ".join([f"{item['name']} x{item['quantity']}" for item in self.cart_items])
        print(food_items_str)

        total = sum(item['price'] * item['quantity'] for item in self.cart_items)
        print("Tổng cộng:", total, "VNĐ")

        from Database.handle import add_food_order
        add_food_order(username, fullname, address, phone, order_status, food_items_str, total)
