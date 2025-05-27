# uiclient/client_app_layout.py
from tkinter import mainloop
import customtkinter as ctk
from uiclient.menu import MenuSidebar
from uiclient.food_list import FoodList
from uiclient.cart import CartView
from uiclient.order_list import OrderList

from PIL import Image, ImageTk  # Thêm để load logo

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Tông màu xanh & chế độ tối/sáng
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Ứng dụng đặt đồ ăn")
        self.geometry("1080x640")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # ===== Header với Logo & tên app =====
        self.header = ctk.CTkFrame(self, fg_color="#0074D9", height=80)  # Màu xanh biển đậm
        self.header.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.header.grid_propagate(False)
        # Logo
        try:
            logo_img = Image.open("logo.png").resize((56,56))
            self.tk_logo = ImageTk.PhotoImage(logo_img)
            self.logo_label = ctk.CTkLabel(self.header, image=self.tk_logo, text="", fg_color="transparent")
            self.logo_label.grid(row=0, column=0, padx=(24, 12), pady=12)
        except Exception as e:
            self.logo_label = ctk.CTkLabel(self.header, text="🍔", font=("Arial", 32), fg_color="transparent")
            self.logo_label.grid(row=0, column=0, padx=(24, 12), pady=12)
        # Tên app
        self.app_name_label = ctk.CTkLabel(self.header, text="FOOD ORDER APP", font=("Arial", 24, "bold"),
                                           text_color="white", fg_color="transparent")
        self.app_name_label.grid(row=0, column=1, padx=0, pady=18, sticky="w")

        # ===== Sidebar (menu trái) =====
        self.menu = MenuSidebar(self)
        self.menu.grid(row=1, column=0, sticky="ns", padx=5, pady=10)

        # ===== Widget chính: danh sách món ăn =====
        self.food_list = FoodList(self)
        self.food_list.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)

        # ===== Widget chính: danh sách đơn hàng =====
        self.order_list = OrderList(self)
        self.order_list.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        self.order_list.grid_remove()  # Ẩn lúc đầu

        # ===== Giỏ hàng bên phải =====
        self.cart = CartView(self)
        self.cart.grid(row=1, column=2, sticky="ns", padx=5, pady=10)

    def show_food_list(self):
        self.food_list.grid()
        self.order_list.grid_remove()

    def show_order_list(self):
        self.order_list.grid()
        self.food_list.grid_remove()