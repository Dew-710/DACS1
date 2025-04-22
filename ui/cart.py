# ui/cart.py
import customtkinter as ctk

class CartView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=250)

        ctk.CTkLabel(self, text="🛒 Giỏ hàng", font=("Arial", 18)).pack(pady=10)
        ctk.CTkLabel(self, text="(Món đã chọn sẽ hiển thị ở đây)").pack()
        ctk.CTkButton(self, text="Đặt hàng", fg_color="green", hover_color="darkgreen").pack(pady=20)
