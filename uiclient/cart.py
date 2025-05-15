import base64
import time
from pyexpat.errors import messages
from tkinter import messagebox

import customtkinter as ctk
from Handle_login_logout.user_session import get_current_user
import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
import threading
# da luong chatgpt


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

        price = float(price)

        # Kiểm tra xem món đã có trong giỏ hàng chưa
        for item in self.cart_items:
            if item["id"] == item_id:
                item["quantity"] += 1
                break
        else:
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

        for widget in self.cart_frame.winfo_children():
            widget.destroy()

        total = 0

        for index, item in enumerate(self.cart_items):
            item_total = item["price"] * item["quantity"]
            total += item_total

            item_frame = ctk.CTkFrame(self.cart_frame)
            item_frame.pack(fill="x", pady=2)

            name_label = ctk.CTkLabel(item_frame, text=f"{item['name']} ({item['price']} VNĐ/món)", width=200, anchor="w")
            name_label.pack(side="left", padx=5)

            qty_label = ctk.CTkLabel(item_frame, text=f"Số lượng: {item['quantity']}", width=100)
            qty_label.pack(side="left")

            minus_btn = ctk.CTkButton(item_frame, text="-", width=30, command=lambda i=index: self.change_quantity(i, -1))
            minus_btn.pack(side="left", padx=2)

            plus_btn = ctk.CTkButton(item_frame, text="+", width=30, command=lambda i=index: self.change_quantity(i, 1))
            plus_btn.pack(side="left", padx=2)

        self.total_label.configure(text=f"Tổng cộng: {total} VNĐ")
        return total

    def change_quantity(self, index, delta):
        item = self.cart_items[index]
        item["quantity"] += delta

        if item["quantity"] <= 0:
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

        food_items_str = ", ".join([f"{item['name']} x{item['quantity']}" for item in self.cart_items])
        total = float(sum(item['price'] * item['quantity'] for item in self.cart_items))




        from Database.handle import add_food_order
        order_id = add_food_order(username, fullname, address, phone, order_status, food_items_str, total)
        print(order_id)


        self.show_payment_qr(total,order_id)
        threading.Thread(target=self.simulate_payment, args=(order_id,), daemon=True).start()

    def show_payment_qr(self, amount,idfood):
        url = "https://api.vietqr.io/v2/generate"

        amount_int = int(round(amount))

        payload = {
            "accountNo": "71006868686868",
            "accountName": "LE HO ANH DUNG",
            "acqId": "970407",
            "addInfo": f"Thanh toan don hang {idfood}",
            "amount": amount_int,
            "template": "compact"
        }

        try:
            response = requests.post(url, json=payload)
            print("Status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                data = response.json().get("data", {})
                qr_data_url = data.get("qrDataURL")
                print("QR Data URL:", qr_data_url)

                if qr_data_url:
                    # qrDataURL dạng: "data:image/png;base64,iVBORw0K..."
                    # Tách lấy phần base64 sau dấu phẩy
                    base64_str = qr_data_url.split(",")[1]

                    # Giải mã base64 thành bytes ảnh
                    img_data = base64.b64decode(base64_str)

                    img = Image.open(BytesIO(img_data))
                    img = img.resize((250, 250))
                    photo = ImageTk.PhotoImage(img)

                    top = ctk.CTkToplevel(self)
                    top.title("Quét mã để thanh toán")
                    top.geometry("300x350")

                    label = ctk.CTkLabel(top, text=f"Thanh toán: {amount_int} VNĐ", font=("Arial", 14))
                    label.pack(pady=10)

                    qr_label = ctk.CTkLabel(top, image=photo)
                    qr_label.image = photo
                    qr_label.pack(pady=10)




                else:
                    print("Không tìm thấy qrDataURL trong phản hồi")
            else:
                print("Lỗi tạo QR:", response.text)

        except Exception as e:
            print("Lỗi khi gọi API VietQR:", e)

    def simulate_payment(self, order_id):


        print(f"Đang kiểm tra đơn hàng {order_id}...")
        time.sleep(10)
        messagebox.showinfo("Thanh toán", f"Thanh toán đơn hàng {order_id} thành công!")
        self.cart_items.clear()
        self.update_cart_view()



        #lỗi đóng cua so widget khiến chuong trình bị break

