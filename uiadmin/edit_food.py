import customtkinter as ctk


class EditFoodFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="✏️ Sửa món ăn", font=("Arial", 24)).pack(pady=20)

        # Form sửa món
        ctk.CTkEntry(self, placeholder_text="Tên món cần sửa").pack(pady=10)
        ctk.CTkEntry(self, placeholder_text="Tên mới").pack(pady=10)
        ctk.CTkEntry(self, placeholder_text="Giá mới").pack(pady=10)
        ctk.CTkButton(self, text="Cập nhật món ăn").pack(pady=10)
