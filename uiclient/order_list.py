import customtkinter as ctk
from Database.handle import get_connection
from Handle_login_logout.user_session import get_current_user, set_current_user


class OrderList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user = get_current_user()
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)
        username = self.user.username
        self.order_items = []
        self.load_order_items(username)




    def load_order_items(self,username):
        try:
            self.cursor.execute(
                "SELECT order_id, order_status, food_item FROM orders WHERE username = %s",
                (username,)
            )
            rows = self.cursor.fetchall()

            for row in rows:
                self.create_order_item(row[0], row[1], row[2])
        except Exception as e:
            print("Lỗi khi lấy dữ liệu:", e)

    def create_order_item(self, order_id, order_status, food_item):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        frame.pack(pady=5, fill="x", padx=10)

        label_text = f"Đơn hàng: {order_id}\nTrạng thái: {order_status}\nMón: {food_item}"
        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14), justify="left")
        label.pack(padx=10, pady=10)

        self.order_items.append({
            "widget": frame,
            "id": order_id,
            "status": order_status,
            "items": food_item
        })

    def _bind_to_mousewheel(self, event=None):
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event=None):
        self.scrollable_frame.unbind("<MouseWheel>")
        self.scrollable_frame.unbind("<Button-4>")
        self.scrollable_frame.unbind("<Button-5>")

    def _on_mousewheel(self, event):
        try:
            if event.num == 5 or event.delta < 0:
                self.scrollable_frame._parent_canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                self.scrollable_frame._parent_canvas.yview_scroll(-1, "units")
        except Exception as e:
            print("Lỗi cuộn chuột:", e)
