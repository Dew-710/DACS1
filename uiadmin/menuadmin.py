import customtkinter as ctk
from uiadmin.queue_list import Queue_list
# từ từ bạn import thêm các frame Thêm/Xóa/Sửa món ăn

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ứng Dụng Quản Lí")
        self.geometry("1000x600")

        self.sidebar = MenuSidebar(self, self.show_frame)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.current_frame = None

    def show_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.main_frame)
        self.current_frame.pack(expand=True, fill="both")

import customtkinter as ctk

class MenuSidebar(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent, width=180)

        self.show_frame_callback = show_frame_callback  # Lưu hàm callback để thay đổi frame

        ctk.CTkLabel(self, text="🍽 Danh mục chức năng", font=("Arial", 18)).pack(pady=10)

        function = ["Duyệt Tài Khoản", "Thêm món ăn", "Xóa món ăn", "Sửa món ăn", "Chỉnh sửa tài khoản"]  # Thêm chức năng "Chỉnh sửa tài khoản"
        for fun in function:
            ctk.CTkButton(self, text=fun, width=200, command=lambda f=fun: self.button_click(f)).pack(pady=5)

    def button_click(self, function_name):
        self.show_frame_callback(function_name)  # Gọi hàm thay đổi frame

