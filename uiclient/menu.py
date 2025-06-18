import customtkinter as ctk
from Handle_login_logout.edit_account_client import EditAccountPopup
from Handle_login_logout.user_session import get_current_user


class MenuSidebar(ctk.CTkFrame):
    def __init__(self, parent):
        from chatbox.client_gui import ChatClient
        super().__init__(parent, width=200, corner_radius=15)
        self.master = parent  # Tham chiếu đến MainApp
        self.ChatClientClass = ChatClient
        self.configure(fg_color="transparent")  # Nền trong suốt nếu dùng theme sáng/tối

        # Nút chỉnh sửa tài khoản
        user = get_current_user()
        ctk.CTkLabel(self, text=f"Xin chào {user.fullname}👋 ", font=("Arial", 16, "bold")).pack(pady=(20, 10))
        ctk.CTkButton(
            self,
            text="👤 Chỉnh sửa tài khoản",
            font=("Arial", 14),
            command=self.edit_account,
            height=40,
            corner_radius=8,fg_color="#00e676", hover_color="#009f4d",
                              text_color="#23272e"
        ).pack(pady=(0, 20), padx=10, fill="x")
        ctk.CTkButton(
            self,
            text="👤 Nhắn Tin",
            font=("Arial", 14),
            command=self.open_chat_client,
            height=40,
            corner_radius=8, fg_color="#00e676", hover_color="#009f4d",
            text_color="#23272e"
        ).pack(pady=(0, 20), padx=10, fill="x")

        # Tiêu đề danh mục
        ctk.CTkLabel(self, text="🍽 Danh mục món ăn", font=("Arial", 18, "bold")).pack(pady=(0, 15))

        # Danh sách danh mục
        categories = ["Tất cả", "Pizza", "Burger", "Mì", "Nước"]
        for cat in categories:
            ctk.CTkButton(
                self,
                text=cat,
                font=("Arial", 13),
                width=160,
                height=35,
                corner_radius=8,
                fg_color="#00e676",
                hover_color="#009f4d",
                text_color="#23272e",
                command=lambda c=cat: self.master.food_list.filter_by_category(c)
            ).pack(pady=5, padx=10)

        # 🆕 Nút đơn hàng
        ctk.CTkLabel(self, text="🧾 Đơn hàng", font=("Arial", 18, "bold")).pack(pady=(30, 10))
        ctk.CTkButton(
            self,
            text="📦 Xem đơn hàng",
            font=("Arial", 13),
            height=40,
            corner_radius=8,
            fg_color="#00e676", hover_color="#009f4d",
            text_color="#23272e",
            command=self.show_orders
        ).pack(pady=5, padx=10, fill="x")

    def edit_account(self):
        EditAccountPopup(self.master)

    def show_orders(self):
        self.master.show_order_list()

    def open_chat_client(self):
        self.ChatClientClass(self.master)