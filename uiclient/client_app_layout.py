# uiclient/client_app_layout.py
from tkinter import mainloop

import customtkinter as ctk
from uiclient.menu import MenuSidebar
from uiclient.food_list import FoodList
from uiclient.cart import CartView


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ứng dụng đặt đồ ăn")
        self.geometry("1080x640")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Sidebar (menu trái)
        self.menu = MenuSidebar(self)
        self.menu.grid(row=0, column=0, sticky="ns", padx=5, pady=10)

        # Khu vực chính - danh sách món ăn
        self.food_list = FoodList(self)
        self.food_list.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

        # Giỏ hàng bên phải
        self.cart = CartView(self)
        self.cart.grid(row=0, column=2, sticky="ns", padx=5, pady=10)

