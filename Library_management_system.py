import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x500")
        
        # Set a background color
        self.root.configure(bg="#f0f0f0")
        
        # Connect to the database and create tables
        self.create_database()
        
        # Login Screen
        self.login_screen()

    def create_database(self):
        self.conn = sqlite3.connect('library_management.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                author TEXT NOT NULL,
                type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                available INTEGER NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                issue_date DATE NOT NULL,
                return_date DATE,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memberships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_name TEXT NOT NULL,
                duration TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL
            )
        ''')
        self.conn.commit()

    def log_action(self, action):
        self.cursor.execute('INSERT INTO logs (action) VALUES (?)', (action,))
        self.conn.commit()

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

        # Check if the user is an admin
        if username == "admin" and password == "admin123":
            self.user_role = "admin"
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            self.main_menu()
            return

        # Check if the user is a regular user
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        result = self.cursor.fetchone()

        if result:
            self.user_role = "user"
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
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
            tk.Button(self.root, text="User  Management", command=self.user_management).pack(pady=10)
            tk.Button(self.root, text="View Logs", command=self.view_logs).pack(pady=10)
        
        tk.Button(self.root, text="Issue Book", command=self.issue_book).pack(pady=10)
        tk.Button(self.root, text="Return Book", command=self.return_book).pack(pady=10)
        tk.Button(self.root, text="Check Book Availability", command=self.check_book_availability).pack(pady=10)
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
        
        tk.Label(self.root, text="Quantity", bg="#f0f0f0").pack(pady=5)
        self.book_quantity = tk.Entry(self.root)
        self.book_quantity.pack(pady=5)
        self.book_quantity.insert(0, "Quantity (required)")
        
        tk.Button(self.root, text="Submit", command=self.submit_add_book).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_add_book(self):
        if not self.book_name.get() or not self.author_name.get() or not self.book_quantity.get():     
            messagebox.showerror("Error", "All fields are mandatory.")
            return
        
        try:
            quantity = int(self.book_quantity.get())
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a valid positive integer.")
            return
        
        self.cursor.execute('INSERT INTO books (name, author, type, quantity, available) VALUES (?, ?, ?, ?, ?)', 
                            (self.book_name.get(), self.author_name.get(), self.book_type.get(), quantity, quantity))
        self.conn.commit()
        self.log_action(f"Added book: {self.book_name.get()} by {self.author_name.get()} with quantity {quantity}")
        messagebox.showinfo("Success", "Book added successfully!")
        self.main_menu() 

    def add_membership(self):
        self.clear_frame()
        tk.Label(self.root, text="Add Membership", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        tk.Label(self.root, text="Member Name", bg="#f0f0f0").pack(pady=5)
        self.member_name_entry = tk.Entry(self.root)
        self.member_name_entry.pack(pady=5)
        self.member_name_entry.insert(0, "Member Name (required)")
        
        self.membership_duration = tk.StringVar(value="6 months")
        tk.Radiobutton(self.root, text="6 Months", variable=self.membership_duration, value="6 months", bg="#f0f0f0").pack()
        tk.Radiobutton(self.root, text="1 Year", variable=self.membership_duration, value="1 year", bg="#f0f0f0").pack()
        tk.Radiobutton(self.root, text="2 Years", variable=self.membership_duration, value="2 years", bg="#f0f0f0").pack()
        
        tk.Button(self.root, text="Submit", command=self.submit_add_membership).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_add_membership(self):
        if not self.member_name_entry.get():
            messagebox.showerror("Error", "Member Name is required.")
            return
        
        start_date = datetime.now().date()
        if self.membership_duration.get() == "6 months":
            end_date = start_date + timedelta(days=182)
        elif self.membership_duration.get() == "1 year":
            end_date = start_date + timedelta(days=365)
        else:  # 2 years
            end_date = start_date + timedelta(days=730)

        self.cursor.execute('INSERT INTO memberships (member_name, duration, start_date, end_date) VALUES (?, ?, ?, ?)', 
                            (self.member_name_entry.get(), self.membership_duration.get(), start_date, end_date))
        self.conn.commit()
        self.log_action(f"Added membership for: {self.member_name_entry.get()} for {self.membership_duration.get()}")
        messagebox.showinfo("Success", "Membership added successfully!")
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
        
        tk.Button(self.root, text="Fetch Author", command=self.fetch_author).pack(pady=10)
        tk.Button(self.root, text="Submit", command=self.submit_issue_book).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def fetch_author(self):
        book_name = self.issue_book_name.get()
        if not book_name:
            messagebox.showerror("Error", "Please enter a book name.")
            return
        
        self.cursor.execute('SELECT author FROM books WHERE name = ?', (book_name,))
        result = self.cursor.fetchone()
        
        if result:
            self.issue_author_name.config(state='normal')  # Enable the entry to set the author
            self.issue_author_name.delete(0, tk.END)  # Clear the entry
            self.issue_author_name.insert(0, result[0])  # Set the author name
            self.issue_author_name.config(state='readonly')  # Set it back to read-only
        else:
            messagebox.showerror("Error", "Book not found.")

    def submit_issue_book(self):
        if not self.issue_book_name.get():
            messagebox.showerror("Error", "Book Name is required.")
            return
        
        # Fetch the book ID based on the book name
        self.cursor.execute('SELECT id, available FROM books WHERE name = ?', (self.issue_book_name.get(),))
        result = self.cursor.fetchone()
        
        if result:
            book_id, available = result
            if available > 0:
                issue_date = datetime.now().date()
                self.cursor.execute('INSERT INTO issued_books (book_id, username, issue_date) VALUES (?, ?, ?)', 
                                    (book_id, "user", issue_date))
                self.cursor.execute('UPDATE books SET available = available - 1 WHERE id = ?', (book_id,))
                self.conn.commit()
                self.log_action(f"Issued book: {self.issue_book_name.get()} to user.")
                messagebox.showinfo("Success", "Book issued successfully!")
                self.main_menu()
            else:
                messagebox.showerror("Error", "No copies available for this book.")
        else:
            messagebox.showerror("Error", "Book not found.")

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
        
        tk.Button(self.root, text="Fetch Author", command=self.fetch_return_author).pack(pady=10)
        tk.Button(self.root, text="Submit", command=self.submit_return_book).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def fetch_return_author(self):
        book_name = self.return_book_name.get()
        if not book_name:
            messagebox.showerror("Error", "Please enter a book name.")
            return
        
        self.cursor.execute('SELECT author FROM books WHERE name = ?', (book_name,))
        result = self.cursor.fetchone()
        
        if result:
            self.return_author_name.config(state='normal')  # Enable the entry to set the author
            self.return_author_name.delete(0, tk.END)  # Clear the entry
            self.return_author_name.insert(0, result[0])  # Set the author name
            self.return_author_name.config(state='readonly')  # Set it back to read-only
        else:
            messagebox.showerror("Error", "Book not found.")

    def submit_return_book(self):
        if not self.return_book_name.get():
            messagebox.showerror("Error", "Book Name is required.")
            return
        
        # Fetch the book ID based on the book name
        self.cursor.execute('SELECT id FROM books WHERE name = ?', (self.return_book_name.get(),))
        result = self.cursor.fetchone()
        
        if result:
            book_id = result[0]
            return_date = datetime.now().date()
            
            # Fetch the issue date from the database
            self.cursor.execute('SELECT issue_date FROM issued_books WHERE book_id = ? AND username = ?', 
                                (book_id, "user"))
            issue_result = self.cursor.fetchone()
            
            if issue_result:
                issue_date = datetime.strptime(issue_result[0], '%Y-%m-%d').date()
                due_date = issue_date + timedelta(days=14)  # Assuming a 14-day loan period
                if return_date > due_date:
                    overdue_days = (return_date - due_date).days
                    fine = overdue_days * 1  # Assuming a fine of $1 per day
                    messagebox.showinfo("Fine", f"You have a fine of ${fine} for returning the book late.")
                else:
                    messagebox.showinfo("Success", "Book returned successfully!")
                self.cursor.execute('UPDATE books SET available = available + 1 WHERE id = ?', (book_id,))
                self.cursor.execute('UPDATE issued_books SET return_date = ? WHERE book_id = ? AND username = ?', 
                                    (return_date, book_id, "user"))
                self.conn.commit()
                self.log_action(f"Returned book: {self.return_book_name.get()} by user.")
            else:
                messagebox.showerror("Error", "No record found for this book.")
        else:
            messagebox.showerror("Error", "Book not found.")
        
        self.main_menu()

    def check_book_availability(self):
        self.clear_frame()
        tk.Label(self.root, text="Check Book Availability", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        self.check_book_name = tk.Entry(self.root)
        self.check_book_name.pack(pady=5)
        self.check_book_name.insert(0, "Book Name (required)")
        
        tk.Button(self.root, text="Check Availability", command=self.submit_check_availability).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_check_availability(self):
        book_name = self.check_book_name.get()
        if not book_name:
            messagebox.showerror("Error", "Book Name is required.")
            return
        
        # Check if the book is issued
        self.cursor.execute('''
            SELECT available FROM books WHERE name = ?
        ''', (book_name,))
        result = self.cursor.fetchone()
        
        if result:
            available = result[0]
            if available > 0:
                messagebox.showinfo("Availability", f"The book '{book_name}' is available for borrowing.")
            else:
                messagebox.showinfo("Availability", f"The book '{book_name}' is currently not available.")
        else:
            messagebox.showerror("Error", "Book not found.")

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
        self.log_action(f"Updated membership number: {self.membership_number.get()}")
        self.main_menu()

    def user_management(self):
        self.clear_frame()
        tk.Label(self.root, text="User  Management", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)
        
        tk.Label(self.root, text="New Username", bg="#f0f0f0").pack(pady=5)
        self.new_user_name = tk.Entry(self.root)
        self.new_user_name.pack(pady=5)
        self.new_user_name.insert(0, "Enter Username (required)")
        
        tk.Label(self.root, text="New Password", bg="#f0f0f0").pack(pady=5)
        self.new_user_password = tk.Entry(self.root, show="*")
        self.new_user_password.pack(pady=5)
        self.new_user_password.insert(0, "Enter Password (required)")
        
        tk.Button(self.root, text="Add User", command=self.submit_user_management).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def submit_user_management(self):
        username = self.new_user_name.get()
        password = self.new_user_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and Password are mandatory.")
            return
        
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.conn.commit()
            self.log_action(f"Added new user: {username}")
            messagebox.showinfo("Success", f"New user '{username}' added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        
        self.main_menu()

    def view_logs(self):
        self.clear_frame()
        tk.Label(self.root, text="Action Logs", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

        # Create a canvas for scrolling
        canvas = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Pack the canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.cursor.execute('SELECT action, timestamp FROM logs ORDER BY timestamp DESC')
        logs = self.cursor.fetchall()
        
        for log in logs:
            tk.Label(scrollable_frame, text=f"{log[1]} - {log[0]}", bg="#f0f0f0").pack(pady=2)

        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

root = tk.Tk()
app = LibraryManagementSystem(root)
root.mainloop()
