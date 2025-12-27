import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import database

database.create_tables()

# ---------------- Functions ----------------
def refresh_students():
    student_list.delete(*student_list.get_children())
    students.clear()

    for s in database.get_students():
        students.append(s)
        student_list.insert("", "end", values=(s[1],))

def add_student():
    name = name_entry.get().strip()
    if not name:
        messagebox.showwarning("Xatolik", "Talaba ismini kiriting")
        return

    database.add_student(name)
    name_entry.delete(0, tk.END)
    refresh_students()

def get_selected_student():
    selected = student_list.focus()
    if not selected:
        messagebox.showwarning("Xatolik", "Talabani tanlang")
        return None
    index = student_list.index(selected)
    return students[index][0]

def mark(status):
    student_id = get_selected_student()
    if student_id:
        database.mark_attendance(
            student_id,
            date.today().isoformat(),
            status
        )
        status_label.config(text=f"Davomat belgilandi: {status}")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Talabalar Davomat Tizimi")
root.geometry("520x420")
root.configure(bg="#f4f6f8")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))

# ---------- Header ----------
header = ttk.Label(root, text="📋 Talabalar Davomat Tizimi", style="Header.TLabel")
header.pack(pady=15)

# ---------- Add student frame ----------
add_frame = ttk.Frame(root)
add_frame.pack(pady=10)

ttk.Label(add_frame, text="Talaba ismi:").grid(row=0, column=0, padx=5)
name_entry = ttk.Entry(add_frame, width=25)
name_entry.grid(row=0, column=1, padx=5)

ttk.Button(add_frame, text="➕ Qo‘shish", command=add_student).grid(row=0, column=2, padx=5)

# ---------- Student list ----------
list_frame = ttk.Frame(root)
list_frame.pack(pady=10, fill="x", padx=20)

columns = ("name",)
student_list = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
student_list.heading("name", text="Talabalar ro‘yxati")
student_list.column("name", anchor="center")

scroll = ttk.Scrollbar(list_frame, orient="vertical", command=student_list.yview)
student_list.configure(yscrollcommand=scroll.set)

student_list.pack(side="left", fill="x", expand=True)
scroll.pack(side="right", fill="y")

# ---------- Buttons ----------
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=15)

ttk.Button(btn_frame, text="✅ BOR", command=lambda: mark("BOR")).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="❌ YO‘Q", command=lambda: mark("YO‘Q")).grid(row=0, column=1, padx=10)

# ---------- Status ----------
status_label = ttk.Label(root, text="", foreground="green")
status_label.pack(pady=10)

students = []
refresh_students()

root.mainloop()
