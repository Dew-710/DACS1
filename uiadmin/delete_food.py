from tkinter import messagebox

import customtkinter as ctk
from Database.handle import get_connection



class DeleteFoodFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        ctk.set_appearance_mode("dark")

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Nhập tên món", textvariable=self.search_var)
        self.search_entry.pack(padx=10, pady=(10, 5), fill="x")
        self.search_entry.bind("<KeyRelease>", self.on_search)



        self.food_items = []
        self.load_food_items()


    def load_food_items(self):
        try:
            self.cursor.execute("SELECT id, name, category, price FROM food")
            rows = self.cursor.fetchall()

            for row in rows:
                self.create_food_item(row[0], row[1], row[2], row[3])
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def create_food_item(self, id, name, category, price):
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(pady=5, fill="x", padx=10)

        label = ctk.CTkLabel(frame, text=f"{id} - {name} - [{category}] - {price} VNĐ", font=("Arial", 14))
        label.pack(padx=10, pady=10)

        delete_button = ctk.CTkButton(
            frame, text="🗑️ Xoá", fg_color="red",
            command=lambda: self.delete_food_from_db(id, frame)
        )
        delete_button.pack(pady=(0, 10))

        self.food_items.append({
            "id": id,
            "widget": frame,
            "name": name,
            "category": category,
            "price": price
        })

    def on_search(self, event=None):
        keyword = self.search_var.get().lower()


        for item in self.food_items:
            item["widget"].pack_forget()


        for item in self.food_items:

            if "name" in item and keyword in item["name"].lower():
                item["widget"].pack(pady=5, fill="x", padx=10)
                print("Tìm kiếm được món:", item["name"])


    def delete_food_from_db(self, food_id, widget):
        confirm = messagebox.askyesno("Xác nhận xoá", "Bạn có chắc chắn muốn xoá món ăn này không?")
        if not confirm:
            return

        try:
            from Database.handle import delete_food
            delete_food(food_id)
            widget.destroy()  # Xoá khỏi giao diện
            self.food_items = [item for item in self.food_items if item["id"] != food_id]
            messagebox.showinfo("Thành công", "Đã xoá món ăn.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xoá món ăn: {e}")
