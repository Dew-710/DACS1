# uiclient/client_app_layout.py
from tkinter import mainloop
import customtkinter as ctk
from uiclient.menu import MenuSidebar
from uiclient.food_list import FoodList
from uiclient.cart import CartView
from uiclient.order_list import OrderList


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Ứng dụng đặt đồ ăn")
        self.geometry("1080x640")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header = ctk.CTkFrame(self, fg_color="#0074D9", height=80)
        self.header.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.header.grid_propagate(False)

        self.app_name_label = ctk.CTkLabel(self.header, text="FOOD ORDER APP", font=("Arial", 24, "bold"),
                                           text_color="white", fg_color="transparent")
        self.app_name_label.grid(row=0, column=0, padx=20, pady=18, sticky="w")

        try:
            self.menu = MenuSidebar(self)
            self.menu.grid(row=1, column=0, sticky="ns", padx=5, pady=10)
            print("MenuSidebar khởi tạo thành công")
        except Exception as e:
            print("Lỗi khởi tạo MenuSidebar:", e)

        try:
            self.food_list = FoodList(self)
            self.food_list.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
            print("FoodList khởi tạo thành công")
        except Exception as e:
            print("Lỗi khởi tạo FoodList:", e)

        try:
            self.order_list = OrderList(self)
            self.order_list.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
            self.order_list.grid_remove()
            print("OrderList khởi tạo thành công")
        except Exception as e:
            print("Lỗi khởi tạo OrderList:", e)

        try:
            self.cart = CartView(self)
            self.cart.grid(row=1, column=2, sticky="ns", padx=5, pady=10)
            print("CartView khởi tạo thành công")
        except Exception as e:
            print("Lỗi khởi tạo CartView:", e)

    def show_food_list(self):
        self.food_list.grid()
        self.order_list.grid_remove()

    def show_order_list(self):
        self.order_list.grid()
        self.food_list.grid_remove()