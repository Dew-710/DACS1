import socket
import threading

from tkinter import messagebox
from Handle_login_logout.user_session import get_current_user
from Database.handle import get_msg

HOST = '127.0.0.1'
PORT = 5051

import customtkinter as ctk

class ServerChatGUI(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user = get_current_user()

        self.text_area = ctk.CTkTextbox(self, width=600, height=400)
        self.text_area.configure(state="disabled", wrap="word")
        self.text_area.pack(padx=10, pady=10, fill="both", expand=True)

        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=(0, 10), fill="x")
        self.entry = ctk.CTkEntry(frame, width=500)
        self.entry.pack(side="left", padx=(0, 5), fill="x", expand=True)
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(frame, text="Gửi", command=self.send_message)
        self.send_button.pack(side="left")

        # Kết nối tới server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới server: {e}")
            return

        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()



        all_messages = get_msg()
        self.text_area.configure(state="normal")
        self.text_area.insert("end", all_messages + "\n")
        self.text_area.configure(state="disabled")

    def send_message(self, event=None):
        from Database.handle import insert_msg
        msg = self.entry.get()
        if msg:
            full_msg = f" [admin] {self.user.username}: {msg}" if self.user else f"Unknown: {msg}"
            try:
                self.sock.sendall(full_msg.encode("utf-8"))
                insert_msg(self.user.username,full_msg)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi gửi tin: {e}")
            self.entry.delete(0, "end")

    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                msg = data.decode("utf-8")
                self.after(0, lambda m=msg: self.display_message(m))
            except:
                break

    def display_message(self, msg):
        self.text_area.configure(state="normal")
        self.text_area.insert("end", msg + "\n")
        self.text_area.yview("end")
        self.text_area.configure(state="disabled")

    def destroy(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        super().destroy()
