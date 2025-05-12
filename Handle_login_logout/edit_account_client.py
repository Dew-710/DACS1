import customtkinter as ctk
import tkinter.messagebox as mb
from Handle_login_logout.user_session import get_current_user, set_current_user
from Handle_login_logout.editaccountadmin import EditAccountFrame

class EditAccountPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Chỉnh sửa tài khoản")
        self.geometry("500x600")

        self.edit_frame = EditAccountFrame(self, logout_callback=self.logout, save_callback=self.on_save)
        self.edit_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.lift()
        self.after(100, self.grab_set)

    def logout(self):
        self.after(100, self.show_logout_confirmation)

    def show_logout_confirmation(self):
        print("Đăng xuất người dùng.")
        set_current_user(None)

        root = self.master
        if root:
            root.quit()
            root.destroy()

    def on_save(self):
        print("Thông tin tài khoản đã lưu từ popup.")
        self.destroy()
