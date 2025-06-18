import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
from Handle_login_logout.user_session import get_current_user

HOST = socket.gethostbyname(socket.gethostname())  # Địa chỉ server
PORT = 5051         # Port server

class ChatClient(tk.Toplevel):
    def __init__(self, master=None):

        super().__init__(master)
        self.user = get_current_user()
        if not self.user:
            messagebox.showerror("Lỗi", "Không thể lấy tên người dùng.")
            self.destroy()
            return
        self.title("Python Chat GUI")
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.text_area.pack(padx=10, pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=(0,10))
        self.entry = tk.Entry(frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        self.entry.bind('<Return>', self.send_message)

        self.send_button = tk.Button(frame, text="Gửi", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Kết nối server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới server: {e}")
            self.destroy()
            return

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            full_msg = f"{self.user.username}: {msg}"
            try:
                self.sock.sendall(full_msg.encode('utf-8'))
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi gửi tin: {e}")
            self.entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                self.text_area.config(state='normal')
                self.text_area.insert(tk.END, data.decode('utf-8') + '\n')
                self.text_area.yview(tk.END)
                self.text_area.config(state='disabled')
            except Exception:
                break

    def on_close(self):
        try:
            self.sock.close()
        except Exception:
            pass
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính nếu chỉ muốn dùng Toplevel
    client = ChatClient(root)
    client.mainloop()