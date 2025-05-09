
from uiadmin.menuadmin import MenuSidebar
import customtkinter as ctk

class MainAppManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x700")
        self.title("Ứng Dụng Quản Lí")

        # Frame sidebar
        self.menuadmin = MenuSidebar(self, self.show_frame)  # truyền self.show_frame
        self.menuadmin.pack(side="left", fill="y")

        # Frame chính để thay đổi nội dung
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(side="right", expand=True, fill="both")

    # MainAppManager
    def show_frame(self, function_name):
        # Xóa nội dung cũ
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Hiện frame mới dựa trên function_name
        if function_name == "Duyệt Tài Khoản":
            from uiadmin.queue_list import Queue_list
            frame = Queue_list(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Thêm món ăn":
            from uiadmin.add_food import AddFoodFrame
            frame = AddFoodFrame(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Xóa món ăn":
            from uiadmin.delete_food import DeleteFoodFrame
            frame = DeleteFoodFrame(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Sửa món ăn":
            from uiadmin.edit_food import EditFoodFrame
            frame = EditFoodFrame(self.content_frame)
            frame.pack(expand=True, fill="both")

        elif function_name == "Chỉnh sửa tài khoản":
            from Handle_login_logout.editaccount import EditAccountFrame
            frame = EditAccountFrame(self.content_frame)
            frame.pack(expand=True, fill="both")
