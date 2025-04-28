import customtkinter as ctk

class MenuSidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=180)

        self.master = parent  # MainApp để gọi food_list

        ctk.CTkLabel(self, text="🍽 Danh mục", font=("Arial", 18)).pack(pady=10)

        categories = ["Tất cả", "Pizza", "Burger", "Mì", "Nước" , "Cứt"]
        for cat in categories:
            ctk.CTkButton(self, text=cat, width=160,
                          command=lambda c=cat: self.master.food_list.filter_by_category(c)).pack(pady=4)
