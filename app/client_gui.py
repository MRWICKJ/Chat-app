import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

nickname = simpledialog.askstring("Nickname", "Please choose a nickname:")

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chat Application")
        master.geometry("400x500")

        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10)
        self.chat_area.config(state=tk.DISABLED)

        self.msg_entry = tk.Entry(master, font=("Arial", 12))
        self.msg_entry.pack(fill=tk.X, padx=10, pady=5)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        client.send(nickname.encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                self.display_message(message)
            except:
                print("Error receiving message.")
                client.close()
                break

    def send_message(self, event=None):

        message = f"{nickname}: {self.msg_entry.get()}"
        self.msg_entry.delete(0, tk.END)  
        client.send(message.encode('utf-8'))

    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state=tk.DISABLED)

root = tk.Tk()
gui = ChatGUI(root)
root.mainloop()
