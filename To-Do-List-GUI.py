import tkinter as tk
import tkinter.messagebox as msg
import json

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except:
        return []
    
tasks = load_tasks()

root = tk.Tk()
root.title("To-Do List")
root.geometry("400x400")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

def add_task():
    task = entry.get()
    if task == "":
        return
    
    tasks.append({"task": task, "done": False})
    save_tasks()
    entry.delete(0, tk.END)
    refresh_list()

add_btn = tk.Button(root, text="Add Task", command=add_task)
add_btn.pack()

def complete_task():
    selected = listbox.curselection()
    if not selected:
        return
    
    index = selected[0]
    tasks[index]['done'] = not tasks[index]['done']
    save_tasks()
    refresh_list()

complete_btn = tk.Button(root, text="Mark Complete/Incomplete", command=complete_task)
complete_btn.pack(pady=5)

def delete_task():
    selected = listbox.curselection()
    if not selected:
        return
    
    index = selected[0]
    if msg.askyesno("Confirm", "Delete this task?"):
        tasks.pop(index)
        save_tasks()
        refresh_list()

delete_btn = tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.pack(pady=5)

def clear_tasks():
    if msg.askyesno("Confirm", "Clear all tasks?"):
        tasks.clear()
        save_tasks()
        refresh_list()

listbox = tk.Listbox(root, width=50)
listbox.pack(pady=50)

def refresh_list():
    listbox.delete(0, tk.END)
    for t in tasks:
        symbol = "✔" if t["done"] else "✘"
        listbox.insert(tk.END, f"{t['task']} {symbol}")

refresh_list()

root.mainloop()