from Database.handle import add_food
import customtkinter as ctk
from tkinter import messagebox
class AddFoodFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(self, text="➕ Thêm món ăn mới", font=("Arial", 24)).pack(pady=20)

        # Lưu các Entry để lấy dữ liệu sau
        self.foodname_entry = ctk.CTkEntry(self, placeholder_text="Tên món ăn")
        self.foodname_entry.pack(pady=10)

        self.combo_category = ctk.CTkComboBox(self, values=["Pizza", "Burger", "Mì", "Nước"])
        self.combo_category.pack(pady=5)


        self.price_entry = ctk.CTkEntry(self, placeholder_text="Giá tiền")
        self.price_entry.pack(pady=10)

        ctk.CTkButton(self, text="Thêm món", command=self.submit).pack(pady=10)


    def submit(self):
        foodname = self.foodname_entry.get()
        category = self.combo_category.get()
        price = self.price_entry.get()
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn sẽ thay đổi chứ?")
        if not confirm:
            return
        success = add_food(foodname, category, price)

        if success:
            messagebox.showinfo("Thành công", "Đã thêm món ăn thành công!")
        else:
            messagebox.showerror("Lỗi", "Thêm món ăn thất bại. Vui lòng thử lại.")

