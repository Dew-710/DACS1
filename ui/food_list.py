import customtkinter as ctk
from Database.handle import get_connection

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

        self.food_items.append({
            "widget": frame,
            "category": category
        })

    def filter_by_category(self, selected_category):
        for item in self.food_items:
            if selected_category == "Tất cả" or item["category"] == selected_category:
                item["widget"].pack(pady=5, fill="x", padx=10)
            else:
                item["widget"].pack_forget()
