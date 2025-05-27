import customtkinter as ctk
from tkinter import messagebox
# from Handle_login_logout.user import add_user_to_db, validate_register_info

def main_register_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("Đăng ký tài khoản")
    root.geometry("440x570")
    root.resizable(False, False)
    root.configure(fg_color="#23272e")

    def register():
        username = entry_username.get().strip()
        password = entry_password.get()
        re_password = entry_re_password.get()
        full_name = entry_fullname.get().strip()
        email = entry_email.get().strip()
        phone = entry_phone.get().strip()

        if not username or not password or not re_password or not full_name:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return
        if password != re_password:
            messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp.")
            return

        # result = add_user_to_db(username, password, full_name, email, phone)
        # if result is True:
        #     messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
        #     root.destroy()
        # else:
        #     messagebox.showerror("Lỗi", f"Đăng ký thất bại: {result}")

        # Demo không kết nối DB
        messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
        root.destroy()
        go_back()

    def go_back():
        root.destroy()
        from Handle_login_logout.login import main_login_window
        main_login_window()

    card = ctk.CTkFrame(root, corner_radius=18, fg_color="#2d333b", width=380, height=490)
    card.place(relx=0.5, rely=0.5, anchor="center")

    label_title = ctk.CTkLabel(card, text="📝 Đăng ký tài khoản mới", font=ctk.CTkFont(size=22, weight="bold"), text_color="#00e676")
    label_title.pack(pady=(24, 18))

    entry_username = ctk.CTkEntry(card, placeholder_text="Tên đăng nhập", font=("Arial", 14), border_width=2, corner_radius=8)
    entry_username.pack(pady=(8, 8), padx=28, fill="x")

    entry_fullname = ctk.CTkEntry(card, placeholder_text="Họ và tên", font=("Arial", 14), border_width=2, corner_radius=8)
    entry_fullname.pack(pady=8, padx=28, fill="x")

    entry_email = ctk.CTkEntry(card, placeholder_text="Email (không bắt buộc)", font=("Arial", 14), border_width=2, corner_radius=8)
    entry_email.pack(pady=8, padx=28, fill="x")

    entry_phone = ctk.CTkEntry(card, placeholder_text="Số điện thoại (không bắt buộc)", font=("Arial", 14), border_width=2, corner_radius=8)
    entry_phone.pack(pady=8, padx=28, fill="x")

    entry_password = ctk.CTkEntry(card, placeholder_text="Mật khẩu", font=("Arial", 14), border_width=2, corner_radius=8, show="*")
    entry_password.pack(pady=(12, 6), padx=28, fill="x")

    entry_re_password = ctk.CTkEntry(card, placeholder_text="Nhập lại mật khẩu", font=("Arial", 14), border_width=2, corner_radius=8, show="*")
    entry_re_password.pack(pady=(0, 16), padx=28, fill="x")

    btn_register = ctk.CTkButton(card, text="Đăng ký", font=("Arial", 15, "bold"), fg_color="#00e676", hover_color="#009f4d",
                                 text_color="#23272e", corner_radius=8, height=40, command=register)
    btn_register.pack(pady=(2, 10), padx=28, fill="x")

    btn_back = ctk.CTkButton(card, text="Quay lại đăng nhập", font=("Arial", 13), fg_color="#353b48", hover_color="#444a58",
                             text_color="#00e676", corner_radius=8, height=36, command=go_back)
    btn_back.pack(pady=(0, 10), padx=28, fill="x")

    label_hint = ctk.CTkLabel(card, text="Vui lòng điền đầy đủ thông tin bắt buộc.", font=("Arial", 10), text_color="#b0b8c1")
    label_hint.pack(pady=(4, 0))

    root.mainloop()