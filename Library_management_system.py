import tkinter as tk
from tkinter import messagebox 
from datetime import datetime, timedelta

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")
        
        # Set a background color
        self.root.configure(bg="#f0f0f0")
        
        # Login Screen
        self.login_screen()

    def login_screen(self):
        self.clear_frame()
        tk.Label(self.root, text="Library Management System", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)
        
        tk.Label(self.root, text="Username", bg="#f0f0f0").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)
        
        tk.Label(self.root, text="Password", bg="#f0f0f0").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.check_login).pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # You can replace these checks with actual authentication logic
        if username == "admin" and password == "admin123":
            self.user_role = "admin"
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            self.main_menu()
        elif username == "user" and password == "user123":
            self.user_role = "user"
            messagebox.showinfo("Login Success", "Welcome, User!")
            self.main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")

    def main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Library Management System", font=("Arial", 20), bg="#f0f0f0").pack(pady=20)
        
        if self.user_role == "admin":
            tk.Button(self.root, text="Add Book", command=self.add_book).pack(pady=10)
            tk.Button(self.root, text="Add Membership", command=self.add_membership).pack(pady=10)
            tk.Button(self.root, text="Update Membership", command=self.update_membership).pack(pady=10)
            tk.Button(self.root, text="User Management", command=self.user_management).pack(pady=10)
        
        tk.Button(self.root, text="Issue Book", command=self.issue_book).pack(pady=10)
        tk.Button(self.root, text="Return Book", command=self.return_book).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_book(self):
        self.clear_frame()
        tk.Label(self.root, text="Add Book", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        self.book_name = tk.Entry(self.root)
        self.book_name.pack(pady=5)
        self.book_name.insert(0, "Book Name (required)")
        
        self.author_name = tk.Entry(self.root)
        self.author_name.pack(pady=5)
        self.author_name.insert(0, "Author Name (required)")
        
        self.book_type = tk.StringVar(value="book")
        tk.Radiobutton(self.root, text="Book", variable=self.book_type, value="book", bg="#f0f0f0").pack()
        tk.Radiobutton(self.root, text="Movie", variable=self.book_type, value="movie", bg="#f0f0f0").pack()
        
        tk.Button(self.root, text="Submit", command=self.submit_add_book).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_add_book(self):
        if not self.book_name.get() or not self.author_name.get():
            messagebox.showerror("Error", "All fields are mandatory.")
            return
        # Logic to add book to the database can be added here
        messagebox.showinfo("Success", "Book added successfully!")
        self.main_menu()

    def issue_book(self):
        self.clear_frame()
        tk.Label(self.root, text="Issue Book", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        self.issue_book_name = tk.Entry(self.root)
        self.issue_book_name.pack(pady=5)
        self.issue_book_name.insert(0, "Book Name (required)")
        
        self.issue_author_name = tk.Entry(self.root)
        self.issue_author_name.pack(pady=5)
        self.issue_author_name.insert(0, "Author Name (auto-filled)")
        self.issue_author_name.config(state='readonly')
        
        tk.Button(self.root, text="Submit", command=self.submit_issue_book).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_issue_book(self):
        if not self.issue_book_name.get():
            messagebox.showerror("Error", "Book Name is required.")
            return
        # Logic to issue book can be added here
        messagebox.showinfo("Success", "Book issued successfully!")
        self.main_menu()

    def return_book(self):
        self.clear_frame()
        tk.Label(self.root, text="Return Book", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        self.return_book_name = tk.Entry(self.root)
        self.return_book_name.pack(pady=5)
        self.return_book_name.insert(0, "Book Name (required)")
        
        self.return_author_name = tk.Entry(self.root)
        self.return_author_name.pack(pady=5)
        self.return_author_name.insert(0, "Author Name (auto-filled)")
        self.return_author_name.config(state='readonly')
        
        tk.Button(self.root, text="Submit", command=self.submit_return_book).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_return_book(self):
        if not self.return_book_name.get():
            messagebox.showerror("Error", "Book Name is required.")
            return
        # Logic to return book can be added here
        messagebox.showinfo("Success", "Book returned successfully!")
        self.main_menu()

    def add_membership(self):
        self.clear_frame()
        tk.Label(self.root, text="Add Membership", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        self.membership_duration = tk.StringVar(value="6 months")
        tk.Radiobutton(self.root, text="6 Months", variable=self.membership_duration, value="6 months", bg="#f0f0f0").pack()
        tk.Radiobutton(self.root, text="1 Year", variable=self.membership_duration, value="1 year", bg="#f0f0f0").pack()
        tk.Radiobutton(self.root, text="2 Years", variable=self.membership_duration, value="2 years", bg="#f0f0f0").pack()
        
        tk.Button(self.root, text="Submit", command=self.submit_add_membership).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_add_membership(self):
        # Logic to add membership can be added here
        messagebox.showinfo("Success", "Membership added successfully!")
        self.main_menu()

    def update_membership(self):
        self.clear_frame()
        tk.Label(self.root, text="Update Membership", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        self.membership_number = tk.Entry(self.root)
        self.membership_number.pack(pady=5)
        self.membership_number.insert(0, "Membership Number (required)")
        
        tk.Button(self.root, text="Submit", command=self.submit_update_membership).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_update_membership(self):
        if not self.membership_number.get():
            messagebox.showerror("Error", "Membership Number is required.")
            return
        # Logic to update membership can be added here
        messagebox.showinfo("Success", "Membership updated successfully!")
        self.main_menu()

    def user_management(self):
        self.clear_frame()
        tk.Label(self.root, text="User Management", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        self.user_type = tk.StringVar(value="new")
        tk.Radiobutton(self.root, text="New User", variable=self.user_type, value="new", bg="#f0f0f0").pack()
        tk.Radiobutton(self.root, text="Existing User", variable=self.user_type, value="existing", bg="#f0f0f0").pack()
        
        self.user_name = tk.Entry(self.root)
        self.user_name.pack(pady=5)
        self.user_name.insert(0, "Name (required)")
        
        tk.Button(self.root, text="Submit", command=self.submit_user_management).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_user_management(self):
        if not self.user_name.get():
            messagebox.showerror("Error", "Name is mandatory.")
            return
        # Logic for user management can be added here
        messagebox.showinfo("Success", "User management action completed!")
        self.main_menu()

root = tk.Tk()
app = LibraryManagementSystem(root)
root.mainloop()
