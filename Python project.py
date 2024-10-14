
import tkinter as tk
from tkinter import messagebox
import json
import os
from PIL import Image, ImageTk

class TodoApp:
    def __init__(self, root):
        # Initialize the main application window
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("400x600")  

        # Load and set the background image
        try:
            image = Image.open(r"C:\Users\lokes\Downloads\code.png")  
            image = image.resize((400, 600), Image.LANCZOS)  
            self.background_image = ImageTk.PhotoImage(image)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image not found.")
            self.background_image = None

        # Create a canvas to hold the background image and other widgets
        self.canvas = tk.Canvas(root, width=400, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Draw the background image on the canvas (if loaded)
        if self.background_image:
            self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Load existing tasks from the JSON file
        self.tasks = self.load_tasks()

        # Title label with a classic cream-white background
        self.title_label = tk.Label(root, text="To-Do List", font=("Georgia", 20, "bold"), bg="white", fg="black")
        self.canvas.create_window(200, 40, window=self.title_label)  # Position title on the canvas

        # Task title entry box with light coffee background
        self.task_title_entry = tk.Entry(root, width=22, font=("Georgia", 14), bd=4, relief="groove", bg="#C4A484")
        self.canvas.create_window(160, 160, window=self.task_title_entry)  # Position title entry on the canvas

        # Add task title button
        self.add_title_button = tk.Button(root, text="Add Task", command=self.add_title, bg="#4CAF50", fg="white", font=("Georgia", 12))
        self.canvas.create_window(340, 160, window=self.add_title_button)  # Position button to the right of title entry

        # Task description entry box
        self.task_desc_entry = tk.Entry(root, width=20, font=("Georgia", 14), bd=4, relief="groove", bg="#C4A484")
        self.canvas.create_window(150, 220, window=self.task_desc_entry)  # Position description entry on the canvas

        # Add task description button
        self.add_desc_button = tk.Button(root, text="Add Description", command=self.add_description, bg="#4CAF50", fg="white", font=("Georgia", 12))
        self.canvas.create_window(335, 220, window=self.add_desc_button)  # Position button to the right of description entry

        # Category entry box
        self.task_category_entry = tk.Entry(root, width=20, font=("Georgia", 14), bd=4, relief="groove", bg="#C4A484")
        self.canvas.create_window(150, 280, window=self.task_category_entry)  # Position category entry on the canvas

        # Add task category button 
        self.add_category_button = tk.Button(root, text="Add Category", command=self.add_category, bg="#4CAF50", fg="white", font=("Georgia", 12))
        self.canvas.create_window(330, 280, window=self.add_category_button)  # Position button to the right of category entry

        # Task listbox to display current tasks with light green background
        self.task_listbox = tk.Listbox(root, width=35, height=5, font=("Georgia", 12), bg="#FFFACD", fg="black")
        self.canvas.create_window(200, 350, window=self.task_listbox)  # Position listbox on the canvas

        # Mark as done button
        self.mark_button = tk.Button(root, text="Mark as Done", command=self.mark_task, bg="#C4A484", fg="black", font=("Georgia", 12))
        self.canvas.create_window(200, 450, window=self.mark_button)  # Position button on the canvas

        # Edit task button
        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task, bg="#C4A484", fg="black", font=("Georgia", 12))
        self.canvas.create_window(200, 490, window=self.edit_button)  # Position button on the canvas

        # Delete task button
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, bg="#C4A484", fg="black", font=("Georgia", 12))
        self.canvas.create_window(200, 530, window=self.delete_button)  # Position button on the canvas

        # Update the task listbox with existing tasks
        self.update_task_listbox()

    def load_tasks(self):
        # Load tasks from JSON file
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                return json.load(file)
        return []

    def save_tasks(self):
        # Save tasks to JSON file
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_title(self):
        title = self.task_title_entry.get()
        if title:
            self.current_task = {"title": title, "description": "", "category": "", "completed": False}
            self.task_title_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Title added! Now add a description and category.")
        else:
            messagebox.showwarning("Warning", "Title cannot be empty.")

    def add_description(self):
        if hasattr(self, 'current_task'):
            description = self.task_desc_entry.get()
            if description:
                self.current_task["description"] = description
                self.task_desc_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Description added! Now add a category.")
            else:
                messagebox.showwarning("Warning", "Description cannot be empty.")
        else:
            messagebox.showwarning("Warning", "Please add a title first.")

    def add_category(self):
        if hasattr(self, 'current_task'):
            category = self.task_category_entry.get()
            if category:
                self.current_task["category"] = category
                self.tasks.append(self.current_task)
                self.update_task_listbox()
                self.save_tasks()
                self.task_category_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Task added successfully!")
                del self.current_task
            else:
                messagebox.showwarning("Warning", "Category cannot be empty.")
        else:
            messagebox.showwarning("Warning", "Please add a title and description first.")

    def edit_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            selected_task = self.tasks[selected_index]
            self.task_title_entry.delete(0, tk.END)
            self.task_title_entry.insert(0, selected_task["title"])
            self.task_desc_entry.delete(0, tk.END)
            self.task_desc_entry.insert(0, selected_task["description"])
            self.task_category_entry.delete(0, tk.END)
            self.task_category_entry.insert(0, selected_task["category"])
            self.current_edit_index = selected_index
            self.current_task = selected_task  # Allow modification of the selected task
            messagebox.showinfo("Editing", "Edit the task details and save.")
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to edit.")

    def mark_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = True
            self.update_task_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to mark as done.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?")
            if confirm:
                del self.tasks[selected_index]
                self.update_task_listbox()
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "You must select a task to delete.")

    
    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "(Done)" if task["completed"] else "(Pending)"
            display_text = f"{task['title']} - {status} - {task['description']} - {task['category']}"
            if task["completed"]:
                display_text = f"✔️ {task['title']} - {task['description']} - {task['category']}"
            self.task_listbox.insert(tk.END, display_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
