import psutil
import tkinter as tk
from tkinter import ttk
import time

def get_cpu_usage():
    while True:
        time.sleep(1)
        cpu_usage_label = tk.Label(root, text=f"Cpu Usage: %{psutil.cpu_percent(1)}")
        cpu_usage_label.place(x=200, y=10)


def get_ram_usage():pass


def disk_usage():pass


root=tk.Tk()
root.title("Görev Yöneticisi")
root.geometry("500x500")


cpu_bar=ttk.Progressbar(master=root,length=100,mode="determinate")
cpu_bar.place(x=50,y=10)

ram_bar=ttk.Progressbar(root)
ram_bar.place(x=50, y=50)

disk_bar=ttk.Progressbar(root)
disk_bar.place(x=50,y=100)

cpu_usage_label=tk.Label(root,text=f"Cpu Usage: ")
cpu_usage_label.place(x=200,y=10)


ram_usage_label=tk.Label(root)
disk_usage_label=tk.Label(root)


get_cpu_usage()
root.mainloop()
