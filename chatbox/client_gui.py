import customtkinter as ctk
from tkinter import messagebox
import socket
import threading
from Handle_login_logout.user_session import get_current_user
from Database.handle import get_msg, insert_msg
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5051

class ChatClient(ctk.CTkToplevel):
    def __init__(self, master=None):

        super().__init__(master)
        self.user = get_current_user()
        if not self.user:
            messagebox.showerror("Lỗi", "Không thể lấy tên người dùng.")
            self.destroy()
            return

        self.title(f"💬 Chat - {self.user.username}")
        self.configure(bg="#2d2f33")
        self.geometry("490x480")
        self.resizable(False, False)

        # Khu vực hiển thị tin nhắn
        self.text_area = ctk.CTkTextbox(
            self, width=480, height=340, font=("Consolas", 11),
            fg_color="#1e1e1e", text_color="#dcdcdc", corner_radius=10
        )
        self.text_area.place(x=12, y=12)
        self.text_area.configure(state="disabled")

        # Khung nhập tin nhắn
        input_frame = ctk.CTkFrame(self, fg_color="#2d2f33", corner_radius=10, width=496, height=60)
        input_frame.place(x=12, y=370)

        self.entry = ctk.CTkEntry(
            input_frame, width=320, height=36, font=("Segoe UI", 11),
            fg_color="#3a3f4b", text_color="#ffffff", border_width=0, corner_radius=10
        )
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 8), pady=12)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            input_frame, text="Gửi", font=("Segoe UI", 10, "bold"),
            command=self.send_message, fg_color="#00b894", text_color="white",
            hover_color="#00a383", corner_radius=20, width=80, height=36
        )
        self.send_button.pack(side="left", padx=(0, 0), pady=12)

        # Hiển thị tin nhắn cũ
        all_messages = get_msg()
        self._append_text(all_messages)

        # Kết nối socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới server: {e}")
            self.destroy()
            return


        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _append_text(self, text):
        self.text_area.configure(state="normal")
        self.text_area.insert("end", text + "\n")
        self.text_area.see("end")
        self.text_area.configure(state="disabled")

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if msg:
            full_msg = f"[{time}][user] {self.user.username}: {msg}"
            msg_insert = f"[user] {self.user.username}: {msg}"
            print(time)
            try:
                self.sock.sendall(full_msg.encode('utf-8'))
                insert_msg(self.user.username, msg_insert)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi gửi tin: {e}")
            self.entry.delete(0, "end")

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                self._append_text(data.decode('utf-8'))
            except Exception:
                break

    def on_close(self):
        try:
            self.sock.close()
        except Exception:
            pass
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk()
    root.withdraw()
    app = ChatClient(root)
    app.mainloop()