import customtkinter as ctk
from tkinter import messagebox
from Database.handle import get_connection

CATEGORY_OPTIONS = ["Pizza", "Burger", "Mì", "Nước"]

class FoodList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.food_items = []
        self.load_food_items()

    def load_food_items(self):
        try:
            self.cursor.execute("SELECT id, name, category, price FROM food")
            for row in self.cursor.fetchall():
                self.create_food_item(*row)
        except Exception as e:
            print("Lỗi khi lấy danh sách món ăn:", e)

    def create_food_item(self, food_id, name, category, price):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(pady=5, fill="x", padx=10)

        info = f"{name} - {category} - {price:.2f}₫"
        ctk.CTkLabel(frame, text=info, font=("Arial", 14)).pack(padx=10, pady=10)

        ctk.CTkButton(
            frame,
            text="✏️ Sửa món",
            command=lambda: self.open_edit_window(food_id, name, category, price, frame)
        ).pack(pady=(0, 10))

        self.food_items.append({"id": food_id, "widget": frame})

    def open_edit_window(self, food_id, name, category, price, frame_ref):
        edit_win = ctk.CTkToplevel(self)
        edit_win.title(f"Sửa món: {name}")
        edit_win.geometry("400x300")

        name_var = ctk.StringVar(value=name)
        price_var = ctk.StringVar(value=str(price))
        category_var = ctk.StringVar(value=category if category in CATEGORY_OPTIONS else CATEGORY_OPTIONS[0])

        ctk.CTkLabel(edit_win, text="Tên món").pack(pady=5)
        name_entry = ctk.CTkEntry(edit_win, textvariable=name_var)
        name_entry.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(edit_win, text="Loại món (Category)").pack(pady=5)
        category_menu = ctk.CTkOptionMenu(edit_win, values=CATEGORY_OPTIONS, variable=category_var)
        category_menu.pack(pady=5, fill="x", padx=10)

        ctk.CTkLabel(edit_win, text="Giá tiền").pack(pady=5)
        price_entry = ctk.CTkEntry(edit_win, textvariable=price_var)
        price_entry.pack(pady=5, fill="x", padx=10)

        def update_food():
            try:
                new_name = name_var.get()
                new_category = category_var.get()
                new_price = float(price_var.get())

                self.cursor.execute(
                    "UPDATE food SET name = %s, category = %s, price = %s WHERE id = %s",
                    (new_name, new_category, new_price, food_id)
                )
                self.conn.commit()

                messagebox.showinfo("Thành công", "Đã cập nhật món ăn!")
                edit_win.destroy()
                frame_ref.destroy()
                self.create_food_item(food_id, new_name, new_category, new_price)

            except Exception as e:
                messagebox.showerror("Lỗi", f"Cập nhật thất bại: {e}")

        ctk.CTkButton(edit_win, text="Lưu thay đổi", command=update_food).pack(pady=15)

