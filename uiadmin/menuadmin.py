import customtkinter as ctk



class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ứng Dụng Quản Lí")
        self.geometry("1000x600")
        ctk.set_appearance_mode("light")

        self.sidebar = MenuSidebar(self, self.show_frame)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.current_frame = None

        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text="👋 Xin chào, chúc bạn một ngày tốt lành!",
            font=("Arial", 20, "bold"),
            text_color="#2c3e50"
        )
        self.welcome_label.pack(pady=50)
        print("✅ Đã tạo label Xin chào")

    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
        if hasattr(self, 'welcome_label'):
            self.welcome_label.pack_forget()

        frame_class = self.frames_dict.get(frame_name)
        if frame_class:
            self.current_frame = frame_class(self.main_frame)
            self.current_frame.pack(expand=True, fill="both")

class MenuSidebar(ctk.CTkFrame):
    def __init__(self, parent, show_frame_callback):
        super().__init__(parent, width=200, corner_radius=12)
        self.show_frame_callback = show_frame_callback

        self.configure(fg_color="transparent")

        ctk.CTkLabel(self, text="📋 Menu chức năng", font=("Arial", 18, "bold")).pack(pady=(20, 15))

        functions = [
            ("👥 Duyệt Tài Khoản", "Duyệt Tài Khoản"),
            ("➕ Thêm món ăn", "Thêm món ăn"),
            ("🗑 Xóa món ăn", "Xóa món ăn"),
            ("✏️ Sửa món ăn", "Sửa món ăn"),
            ("👤 Tài Khoản", "Chỉnh sửa tài khoản"),
            ("📦 Quản lí Đơn Đặt Hàng", "Quản lí Đơn Đặt Hàng"),
            ("Thống kê phân tích ", "Thống kê")
        ]

        for label, func_key in functions:
            ctk.CTkButton(
                self,
                text=label,
                font=("Arial", 14),
                height=40,
                corner_radius=8,
                command=lambda f=func_key: self.button_click(f)
            ).pack(pady=6, padx=10, fill="x")

    def button_click(self, function_name):
        self.show_frame_callback(function_name)

