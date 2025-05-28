# uiadmin/admin_app_layout.py
from uiadmin.menuadmin import MenuSidebar
import customtkinter as ctk
from PIL import Image, ImageTk  # Thêm để load logo

class MainAppManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.geometry("1200x700")
        self.title("Ứng Dụng Quản Lí")

        self.header = ctk.CTkFrame(self, fg_color="#0074D9", height=80)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        try:
            logo_img = Image.open("/home/dew/DACS1/pngtree-fresh-hamburger-with-cheese-png-image_14563117.png").resize((56,56))
            self.tk_logo = ImageTk.PhotoImage(logo_img)
            self.logo_label = ctk.CTkLabel(self.header, image=self.tk_logo, text="", fg_color="transparent")
            self.logo_label.pack(side="left", padx=(24, 12), pady=12)
        except Exception as e:
            self.logo_label = ctk.CTkLabel(self.header, text="🧑‍💼", font=("Arial", 32), fg_color="transparent")
            self.logo_label.pack(side="left", padx=(24, 12), pady=12)

        self.app_name_label = ctk.CTkLabel(self.header, text="ADMIN DASHBOARD", font=("Arial", 24, "bold"),
                                           text_color="white", fg_color="transparent")
        self.app_name_label.pack(side="left", padx=0, pady=18)

        self.menuadmin = MenuSidebar(self, self.show_frame)
        self.menuadmin.pack(side="left", fill="y", padx=0, pady=(8,0))


        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", expand=True, fill="both", padx=12, pady=10)

    def show_frame(self, function_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if function_name == "Duyệt Tài Khoản":
            from uiadmin.queue_list import Queue_list
            frame = Queue_list(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Thêm món ăn":
            from uiadmin.add_food import AddFoodFrame
            frame = AddFoodFrame(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Xóa món ăn":
            from uiadmin.delete_food import DeleteFoodFrame
            frame = DeleteFoodFrame(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Sửa món ăn":
            from uiadmin.edit_food import FoodList
            frame = FoodList(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Chỉnh sửa tài khoản":
            from Handle_login_logout.editaccountadmin import EditAccountFrame
            frame = EditAccountFrame(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Quản lí Đơn Đặt Hàng":
            from uiadmin.order import Order_list
            frame = Order_list(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Thống kê":
            from uiadmin.analyze import App
            frame = App(self.content_frame)
            frame.pack(expand=True, fill="both")