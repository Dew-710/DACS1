import customtkinter as ctk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from Handle_login_logout.user_session import set_current_user
from Database.handle import validate_user, get_user_by_email, update_user_password
import threading

from chatbox.server_socket import run_server

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()



EMAIL_ADDRESS = "lehoanhdung710@gmail.com"
EMAIL_PASSWORD = "kpia goup emym krtm"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_reset_code(email, reset_code):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = "Password Reset Code"
        body = f"Mã để cập nhật mật khẩu là: {reset_code}\n.Code sẽ tồn tại trong vòng 30s."
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_reset_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def main_login_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    root = ctk.CTk()
    root.title("Đăng nhập")
    root.geometry("420x500")
    root.resizable(False, False)
    root.configure(fg_color="#23272e")

    current_user = None
    reset_code = None
    reset_email = None

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
            if user.role == ("user"):
                open_main_app()
            elif user.role == "admin":
                openLoginAppbyAdmin()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản, mật khẩu hoặc tài khoản đã bị khóa.")

    def register():
        root.destroy()
        open_register()

    def forgot_password():
        def submit_email():
            nonlocal reset_code, reset_email
            email = entry_email.get()
            if not email:
                messagebox.showerror("Lỗi", "Vui lòng nhập email.")
                return

            user = get_user_by_email(email)
            if not user:
                messagebox.showerror("Lỗi", "Email không tồn tại.")
                return

            reset_code = generate_reset_code()
            reset_email = email
            if send_reset_code(email, reset_code):
                messagebox.showinfo("Thành công", "Mã đặt lại đã được gửi đến email của bạn.")
                email_window.destroy()
                open_reset_password_window()
            else:
                messagebox.showerror("Lỗi", "Không thể gửi email. Vui lòng thử lại.")

        email_window = ctk.CTkToplevel(root)
        email_window.title("Quên mật khẩu")
        email_window.geometry("350x200")
        email_window.resizable(False, False)
        email_window.configure(fg_color="#23272e")

        label_email = ctk.CTkLabel(email_window, text="Nhập email của bạn", font=("Arial", 14))
        label_email.pack(pady=(20, 10))
        entry_email = ctk.CTkEntry(email_window, placeholder_text="Email", font=("Arial", 14), width=250)
        entry_email.pack(pady=10)
        btn_submit = ctk.CTkButton(email_window, text="Gửi mã", command=submit_email, fg_color="#00e676", hover_color="#009f4d")
        btn_submit.pack(pady=10)

    def open_reset_password_window():
        def verify_and_reset():
            code = entry_code.get()
            new_password = entry_new_password.get()
            confirm_password = entry_confirm_password.get()

            if code != reset_code:
                messagebox.showerror("Lỗi", "Mã đặt lại không đúng.")
                return
            if not new_password or not confirm_password:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
                return
            if new_password != confirm_password:
                messagebox.showerror("Lỗi", "Mật khẩu không khớp.")
                return

            if update_user_password(reset_email, new_password):
                messagebox.showinfo("Thành công", "Đặt lại mật khẩu thành công. Vui lòng đăng nhập.")
                reset_window.destroy()
                root.destroy()
                main_login_window()
            else:
                messagebox.showerror("Lỗi", "Không thể cập nhật mật khẩu. Vui lòng thử lại.")

        reset_window = ctk.CTkToplevel(root)
        reset_window.title("Đặt lại mật khẩu")
        reset_window.geometry("450x500")
        reset_window.resizable(False, False)
        reset_window.configure(fg_color="#23272e")

        label_code = ctk.CTkLabel(reset_window, text="Nhập mã đặt lại", font=("Arial", 14))
        label_code.pack(pady=(20, 10))
        entry_code = ctk.CTkEntry(reset_window, placeholder_text="Mã đặt lại", font=("Arial", 14), width=250)
        entry_code.pack(pady=10)

        label_new_password = ctk.CTkLabel(reset_window, text="Mật khẩu mới", font=("Arial", 14))
        label_new_password.pack(pady=10)
        entry_new_password = ctk.CTkEntry(reset_window, placeholder_text="Mật khẩu mới", font=("Arial", 14), width=250, show="*")
        entry_new_password.pack(pady=10)

        label_confirm_password = ctk.CTkLabel(reset_window, text="Xác nhận mật khẩu", font=("Arial", 14))
        label_confirm_password.pack(pady=10)
        entry_confirm_password = ctk.CTkEntry(reset_window, placeholder_text="Xác nhận mật khẩu", font=("Arial", 14), width=250, show="*")
        entry_confirm_password.pack(pady=10)

        btn_reset = ctk.CTkButton(reset_window, text="Đặt lại mật khẩu", command=verify_and_reset, fg_color="#00e676", hover_color="#009f4d")
        btn_reset.pack(pady=10)

    card = ctk.CTkFrame(root, corner_radius=18, fg_color="#2d333b", width=360, height=400)
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

    btn_forgot = ctk.CTkButton(card, text="Quên mật khẩu?", font=("Arial", 13), fg_color="transparent", hover_color="#444a58",
                               text_color="#00e676", corner_radius=8, height=36, command=forgot_password)
    btn_forgot.pack(pady=(0, 10), padx=28, fill="x")

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

if __name__ == "__main__":

    main_login_window()
