import customtkinter as ctk
from tkinter import messagebox
from uiclient.client_app_layout import MainApp

from Database.handle import validate_user


def main_login_window():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Tạo cửa sổ chính
    root = ctk.CTk()
    root.title("Đăng nhập")
    root.geometry("400x400")

    def login():
        username = entry_username.get()
        password = entry_password.get()
        role = validate_user(username,password)
        if role!="none":
            if role == "client":
                root.destroy()
                open_main_app()
            elif role == "admin":
                root.destroy()
                openLoginAppbyAdmin()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu.")
    def register():
        root.withdraw()
        open_register()
    # Giao diện
    label_title = ctk.CTkLabel(root, text="Đăng nhập hệ thống", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=20)

    entry_username = ctk.CTkEntry(root, placeholder_text="Tài khoản")
    entry_username.pack(pady=5)

    entry_password = ctk.CTkEntry(root, placeholder_text="Mật khẩu", show="*")
    entry_password.pack(pady=10)

    btn_login = ctk.CTkButton(root, text="Đăng nhập", command=login)
    btn_login.pack(pady=5)
    root.bind('<Return>', lambda event: login())
      # Nhấn Enter để đăng nhập
    btn_register = ctk.CTkButton(root, text="Đăng kí", command=register)
    btn_register.pack(pady=0)
    root.mainloop()

def open_main_app():
    app = MainApp()
    app.mainloop()
def open_register():
    from uiclient.register import main_register_window
    main_register_window()
def openLoginAppbyAdmin():
    from uiadmin.admin_app_layout import MainAppManager
    app = MainAppManager()
    app.mainloop()