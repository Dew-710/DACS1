import customtkinter as ctk
from Database.handle import get_connection


class FoodList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Tìm món ăn...", textvariable=self.search_var)
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
        add_button = ctk.CTkButton(
            frame, text="Thêm vào giỏ",
            command=lambda: self.master.cart.add_item_to_cart(id, name, category, price)
        )
        add_button.pack(pady=(0, 10))

        self.food_items.append({
            "widget": frame,
            "name": name,
            "category": category,  # Danh mục món ăn
            "price": price  # Giá món ăn
        })

    def filter_by_category(self, selected_category):
        for item in self.food_items:
            if selected_category == "Tất cả" or item["category"] == selected_category:
                item["widget"].pack(pady=5, fill="x", padx=10)
            else:
                item["widget"].pack_forget()

    def on_search(self, event=None):
        keyword = self.search_var.get().lower()


        for item in self.food_items:
            item["widget"].pack_forget()


        for item in self.food_items:

            if "name" in item and keyword in item["name"].lower():
                item["widget"].pack(pady=5, fill="x", padx=10)
                print("Tìm kiếm được món:", item["name"])




