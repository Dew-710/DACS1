import customtkinter as ctk
from tkinter import messagebox
from Handle_login_logout.user_session import set_current_user

from Database.handle import validate_user

def main_login_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("Đăng nhập")
    root.geometry("420x500")
    root.resizable(False, False)
    root.configure(fg_color="#23272e")

    current_user = None

    def login():
        nonlocal current_user
        username = entry_username.get()
        password = entry_password.get()
        user = validate_user(username, password)

        if user:
            current_user = user
            set_current_user(user)
            print("Đăng nhập thành công:", current_user)
            root.destroy()
            if user.role == "client":
                open_main_app()
            elif user.role == "admin":
                openLoginAppbyAdmin()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản, mật khẩu hoặc tài khoản đã bị khóa.")

    def register():
        root.destroy()
        open_register()

    card = ctk.CTkFrame(root, corner_radius=18, fg_color="#2d333b", width=360, height=370)
    card.place(relx=0.5, rely=0.5, anchor="center")

    label_title = ctk.CTkLabel(card, text=" Đăng nhập hệ thống ", font=ctk.CTkFont(size=22, weight="bold"), text_color="#00e676")
    label_title.pack(pady=(24, 12))

    entry_username = ctk.CTkEntry(card, placeholder_text="Tên đăng nhập", font=("Arial", 14), border_width=2, corner_radius=8)
    entry_username.pack(pady=(16, 8), padx=28, fill="x")

    entry_password = ctk.CTkEntry(card, placeholder_text="Mật khẩu", font=("Arial", 14), border_width=2, corner_radius=8, show="*")
    entry_password.pack(pady=(0, 18), padx=28, fill="x")

    btn_login = ctk.CTkButton(card, text="Đăng nhập", font=("Arial", 14, "bold"), fg_color="#00e676", hover_color="#009f4d",
                              text_color="#23272e", corner_radius=8, height=40, command=login)
    btn_login.pack(pady=(2, 12), padx=28, fill="x")
    root.bind('<Return>', lambda event: login())

    btn_register = ctk.CTkButton(card, text="Đăng ký tài khoản mới", font=("Arial", 13), fg_color="#353b48", hover_color="#444a58",
                                 text_color="#00e676", corner_radius=8, height=36, command=register)
    btn_register.pack(pady=(0, 10), padx=28, fill="x")

    label_hint = ctk.CTkLabel(card, text="Quên mật khẩu? Liên hệ quản trị viên.", font=("Arial", 10), text_color="#b0b8c1")
    label_hint.pack(pady=(10, 0))

    root.mainloop()


def open_main_app():
    from uiclient.client_app_layout import MainApp
    app = MainApp()
    app.mainloop()

def open_register():
    from Handle_login_logout.register import main_register_window
    main_register_window()

def openLoginAppbyAdmin():
    from uiadmin.admin_app_layout import MainAppManager
    app = MainAppManager()
    app.mainloop()