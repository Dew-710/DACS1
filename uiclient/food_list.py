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

        # Scrollable area
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Kích hoạt cuộn chuột khi hover
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

        self.food_items = []
        self.current_category = "tất cả"  # Lưu danh mục hiện tại
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
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
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
            "category": category,
            "price": price
        })

    def filter_by_category(self, selected_category):
        print(f"[LỌC] Danh mục: {selected_category}")
        self.current_category = selected_category.lower()
        self.apply_filters()

    def on_search(self, event=None):
        self.apply_filters()

    def apply_filters(self):
        keyword = self.search_var.get().lower()
        selected_clean = self.current_category.strip().lower()

        for item in self.food_items:
            name_match = keyword in item["name"].lower()
            category_match = selected_clean == "tất cả" or item["category"].strip().lower() == selected_clean

            if name_match and category_match:
                item["widget"].pack(pady=5, fill="x")
            else:
                item["widget"].pack_forget()

    def _bind_to_mousewheel(self, event=None):
        # Bind chỉ trên scrollable_frame hoặc trên _parent_canvas (canvas chứa frame)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        # Với Linux, cũng có thể bind <Button-4> và <Button-5> trên scrollable_frame:
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event=None):
        # Unbind các sự kiện trên scrollable_frame thôi
        self.scrollable_frame.unbind("<MouseWheel>")
        self.scrollable_frame.unbind("<Button-4>")
        self.scrollable_frame.unbind("<Button-5>")

    def _on_mousewheel(self, event):
        # event.delta trên Windows/macOS, event.num trên Linux
        try:
            if event.num == 5 or event.delta < 0:
                self.scrollable_frame._parent_canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                self.scrollable_frame._parent_canvas.yview_scroll(-1, "units")
        except Exception as e:
            print("Lỗi cuộn chuột:", e)