import customtkinter as ctk


class AddFoodFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="➕ Thêm món ăn mới", font=("Arial", 24)).pack(pady=20)

        # Ví dụ form thêm món
        ctk.CTkEntry(self, placeholder_text="Tên món ăn").pack(pady=10)
        ctk.CTkEntry(self, placeholder_text="Loại món ăn").pack(pady=10)
        ctk.CTkEntry(self, placeholder_text="Giá tiền").pack(pady=10)
        ctk.CTkButton(self, text="Thêm món").pack(pady=10)
