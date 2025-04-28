import customtkinter as ctk
from tkinter import messagebox
from Database.handle import check_user_exists, Queue_add
from Database.handle import add_user
from validate_email_address import validate_email



def main_register_window():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")


    root = ctk.CTk()
    root.title("Đăng nhập")
    root.geometry("400x400")
    def register():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        email = entry_email.get().strip()
        fullname = entry_fullname.get().strip()
        phone = entry_phone.get().strip()
        role = combo_role.get().strip()
        if not username or not password or not email or not fullname or not phone or not role:
            messagebox.showinfo("Lỗi", "Vui lòng nhập đủ thông tin!")
        elif check_user_exists(username):
            messagebox.showinfo("Lỗi" ,"Tài Khoản Đã Tồn Tại!")
        elif not validate_email(email) :
            messagebox.showinfo("lỗi", "Email chưa đúng định dạng")
        elif role == "admin":
            messagebox.showinfo("Thông báo", "Bạn cần thời gian để được duyệt!")
            Queue_add(username,password,fullname,email,phone)
            open_login_app()
        elif add_user(username,password,fullname,email,phone,role):
            messagebox.showinfo("Thành Công!" , "Đã Tạo Tài Khoản!")
            root.destroy()
            open_login_app()


    label_title = ctk.CTkLabel(root, text="Đăng kí hệ thống", font=ctk.CTkFont(size=20, weight="bold"))
    label_title.pack(pady=20)

    entry_username = ctk.CTkEntry(root, placeholder_text="Tài khoản")
    entry_username.pack(pady=5)

    entry_password = ctk.CTkEntry(root, placeholder_text="Mật khẩu", show="*")
    entry_password.pack(pady=5)

    entry_fullname = ctk.CTkEntry(root, placeholder_text="Họ và tên")
    entry_fullname.pack(pady=5)

    entry_email = ctk.CTkEntry(root, placeholder_text="Email")
    entry_email.pack(pady=5)

    entry_phone = ctk.CTkEntry(root, placeholder_text="Số điện thoại")
    entry_phone.pack(pady=5)

    combo_role = ctk.CTkComboBox(root, values=["client", "admin"])
    combo_role.pack(pady=5)
    combo_role.set("client")

    btn_login = ctk.CTkButton(root, text="Đăng kí", command=register)
    btn_login.pack(pady=20)

    root.bind('<Return>', lambda event: register())
    root.mainloop()

    btn_login = ctk.CTkButton(root, text="Đăng kí", command=register)
    btn_login.pack(pady=20)
    root.bind('<Return>', lambda event: register())
    root.mainloop()
def open_login_app():
    from uiclient.login import main_login_window
    main_login_window()

