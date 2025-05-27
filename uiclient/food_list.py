import customtkinter as ctk
from Database.handle import get_connection

class FoodList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        try:
            self.conn = get_connection()
            self.cursor = self.conn.cursor()
        except Exception as db_err:
            print("Lỗi kết nối CSDL:", db_err)
            ctk.CTkLabel(self, text=f"Lỗi kết nối CSDL: {db_err}", text_color="red").pack()
            return

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Tìm món ăn...", textvariable=self.search_var)
        self.search_entry.pack(padx=10, pady=(10, 5), fill="x")
        self.search_entry.bind("<KeyRelease>", self.on_search)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

        self.food_items = []
        self.current_category = "tất cả"
        self.load_food_items()

    def load_food_items(self):
        try:
            self.cursor.execute("SELECT id, name, category, price FROM food")
            rows = self.cursor.fetchall()
            if not rows:
                ctk.CTkLabel(self.scrollable_frame, text="Chưa có dữ liệu món ăn!", text_color="orange").pack()
            for row in rows:
                self.create_food_item(row[0], row[1], row[2], row[3])
        except Exception as e:
            print("Lỗi lấy dữ liệu:", e)
            ctk.CTkLabel(self.scrollable_frame, text=f"Lỗi lấy dữ liệu: {e}", text_color="red").pack()

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
        # Bind mouse wheel events for different platforms
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)  # Windows
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)  # Linux scroll down

    def _unbind_from_mousewheel(self, event=None):
        # Unbind mouse wheel events
        self.scrollable_frame.unbind("<MouseWheel>")
        self.scrollable_frame.unbind("<Button-4>")
        self.scrollable_frame.unbind("<Button-5>")

    def _on_mousewheel(self, event):
        print("Thuộc tính của scrollable_frame:", dir(self.scrollable_frame))
        try:
            if event.delta:
                scroll_amount = -1 if event.delta > 0 else 1
            elif event.num == 4:
                scroll_amount = -1
            elif event.num == 5:
                scroll_amount = 1
            else:
                return
            # Thử _canvas
            self.scrollable_frame._canvas.yview_scroll(scroll_amount, "units")
            # Hoặc thử trực tiếp
            # self.scrollable_frame.yview_scroll(scroll_amount, "units")
        except AttributeError as e:
            print("Lỗi truy cập canvas/yview_scroll:", e)
        except Exception as e:
            print("Lỗi cuộn chuột:", e)