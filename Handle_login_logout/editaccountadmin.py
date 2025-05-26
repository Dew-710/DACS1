import sys
import os
import customtkinter as ctk
from Database.handle import update_user_info

from Handle_login_logout.user_session import get_current_user, set_current_user


class EditAccountFrame(ctk.CTkFrame):
    def __init__(self, parent, logout_callback=None, save_callback=None):
        super().__init__(parent)
        self.user = get_current_user()
        print("Current user:", self.user)

        self.logout_callback = logout_callback
        self.save_callback = save_callback
        self.user = get_current_user()

        self.title_label = ctk.CTkLabel(self, text="Chỉnh sửa thông tin tài khoản", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=20)

        # Avatar
        self.avatar_frame = ctk.CTkFrame(self, width=100, height=100)
        self.avatar_frame.pack(pady=10)
        self.avatar_label = ctk.CTkLabel(self.avatar_frame, text="No Avatar", width=100, height=100,
                                         corner_radius=50, fg_color="gray", font=("Arial", 16))
        self.avatar_label.pack(padx=10, pady=10)

        # Form nhập thông tin
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=50, fill="x")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Tài khoản (không cho chỉnh sửa)
        self.username_label = ctk.CTkLabel(self.input_frame, text="Tài khoản:")
        self.username_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.username_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Chưa đăng nhập.")
        self.username_entry.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        if self.user:
            self.username_entry.insert(0, self.user.username)
            self.username_entry.configure(state="disabled")

        # Mật khẩu
        self.password_label = ctk.CTkLabel(self.input_frame, text="Mật khẩu:")
        self.password_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.password_entry = ctk.CTkEntry(self.input_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        # Email
        self.email_label = ctk.CTkLabel(self.input_frame, text="Email:")
        self.email_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.email_entry = ctk.CTkEntry(self.input_frame)
        self.email_entry.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        # Số điện thoại
        self.phone_label = ctk.CTkLabel(self.input_frame, text="Số điện thoại:")
        self.phone_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self.input_frame)
        self.phone_entry.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        # Địa chỉ
        self.address_label = ctk.CTkLabel(self.input_frame, text="Địa chỉ:")
        self.address_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        self.address_entry = ctk.CTkEntry(self.input_frame)
        self.address_entry.grid(row=4, column=1, pady=10, padx=10, sticky="ew")

        # Nếu có user thì điền dữ liệu sẵn
        if self.user:
            self.email_entry.insert(0, self.user.email)
            self.phone_entry.insert(0, self.user.phone)
            self.address_entry.insert(0, self.user.address)

        # Nút lưu
        self.save_button = ctk.CTkButton(self, text="Lưu", command=self.save_info)
        self.save_button.pack(pady=(20, 10))

        # Nút đăng xuất
        self.logout_button = ctk.CTkButton(self, text="Đăng xuất", fg_color="red", command=self.logout)
        self.logout_button.pack()

    def save_info(self):
        if self.user:
            # Cập nhật thông tin của user trong đối tượng User
            self.user.update_info(
                password=self.password_entry.get(),
                email=self.email_entry.get(),
                phone=self.phone_entry.get(),
                address=self.address_entry.get()
            )

            # Cập nhật thông tin vào cơ sở dữ liệu
            update_user_info(
                username = self.user.username,
                password=self.user.password,
                email=self.user.email,
                phone=self.user.phone,
                address=self.user.address
            )

            print("Thông tin đã được cập nhật:")
            print(f"Email: {self.user.email}, SDT: {self.user.phone}, Địa chỉ: {self.user.address}")

        if self.save_callback:
            self.save_callback()
    def logout(self):
        print("Đăng xuất người dùng.")
        set_current_user(None)
        if self.logout_callback:
            self.logout_callback()
        else:
            self.master.destroy()
