import customtkinter as ctk
from tkinter import messagebox
from Database.handle import check_user_exists
from Database.handle import add_user



def main_register_window():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")


    root = ctk.CTk()
    root.title("Đăng nhập")
    root.geometry("1000x600")
    def register():
        username = entry_username.get()
        password = entry_password.get()
        if check_user_exists(username):
            messagebox.showinfo("Lỗi" ,"Tài Khoản Đã Tồn Tại!")
        elif add_user(username,password):
            messagebox.showinfo("Thành Công!" , "Đã Tạo Tài Khoản!")
            open_login_app()
            root.destroy()







    label_title = ctk.CTkLabel(root, text="Đăng kí hệ thống", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=20)

    entry_username = ctk.CTkEntry(root, placeholder_text="Tài khoản")
    entry_username.pack(pady=10)

    entry_password = ctk.CTkEntry(root, placeholder_text="Mật khẩu", show="*")
    entry_password.pack(pady=10)

    btn_login = ctk.CTkButton(root, text="Đăng kí", command=register)
    btn_login.pack(pady=20)
    root.bind('<Return>', lambda event: register())
    root.mainloop()
def open_login_app():
    from ui.login import main_login_window
    main_login_window()