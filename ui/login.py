import customtkinter as ctk
from tkinter import messagebox
from ui.app_layout import MainApp

from Database.handle import validate_user


def main_login_window():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")

    # Tạo cửa sổ chính
    root = ctk.CTk()
    root.title("Đăng nhập")
    root.geometry("1000x600")

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if validate_user(username, password):
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            root.destroy()  # Đóng cửa sổ đăng nhập
            open_main_app()  # Mở ứng dụng chính
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu.")
    def register():
        messagebox.showinfo("Thành công", "Đã chuyển qua giao diện đăng kí")
        root.destroy()
        open_register()
    # Giao diện
    label_title = ctk.CTkLabel(root, text="Đăng nhập hệ thống", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=20)

    entry_username = ctk.CTkEntry(root, placeholder_text="Tài khoản")
    entry_username.pack(pady=10)

    entry_password = ctk.CTkEntry(root, placeholder_text="Mật khẩu", show="*")
    entry_password.pack(pady=10)

    btn_login = ctk.CTkButton(root, text="Đăng nhập", command=login)
    btn_login.pack(pady=20)
      # Nhấn Enter để đăng nhập
    btn_login = ctk.CTkButton(root, text="Đăng kí", command=register)
    btn_login.pack(pady=0)
    root.mainloop()

def open_main_app():
    app = MainApp()  # Tạo cửa sổ chính
    app.mainloop()  # Chạy mainloop cho cửa sổ chính
def open_register():
    from ui.register import main_register_window
    main_register_window()