import customtkinter as ctk


class DeleteFoodFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="🗑 Xóa món ăn", font=("Arial", 24)).pack(pady=20)

        # Form nhập món cần xóa
        ctk.CTkEntry(self, placeholder_text="Nhập tên món cần xóa").pack(pady=10)
        ctk.CTkButton(self, text="Xóa món").pack(pady=10)
