import customtkinter as ctk
from Handle_login_logout.edit_account_client import EditAccountPopup
class MenuSidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=180)

        self.master = parent  # MainApp để gọi food_list

        # Nút chỉnh sửa tài khoản - ở trên cùng
        ctk.CTkButton(self, text="👤 Tài khoản", command=self.edit_account).pack(pady=(15, 5), padx=10, fill="x")

        ctk.CTkLabel(self, text="🍽 Danh mục", font=("Arial", 18)).pack(pady=10)

        categories = ["Tất cả", "Pizza", "Burger", "Mì", "Nước"]
        for cat in categories:
            ctk.CTkButton(self, text=cat, width=160,
                          command=lambda c=cat: self.master.food_list.filter_by_category(c)).pack(pady=4)

      # đảm bảo import đúng đường dẫn

    def edit_account(self):
        EditAccountPopup(self.master)



