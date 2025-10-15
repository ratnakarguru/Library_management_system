# Library Management System (LMS) - Python Tkinter Application

## Overview

The **Library Management System** is a desktop-based application built using Python's `tkinter` library and SQLite for data persistence. It provides a simple yet functional interface for managing library operations such as book inventory, membership handling, issuing and returning books, and user authentication. The system supports role-based access: **Admin** and **Regular Users**, with distinct privileges.

This application simulates real-world library workflows with features like fine calculation on overdue returns, action logging, and membership tracking. It uses a local SQLite database (`library_management.db`) to store all data persistently across sessions.

---

## Features

### User Authentication
- **Login System**: 
  - Default admin: `admin` / `admin123`
  - Regular users can be added via admin panel.
- Passwords stored in plain text (for demo purposes only; not secure for production).
- Role-based UI customization.

### Admin Features
- **Add Books**: Add books or movies with name, author, type, and quantity.
- **Add Memberships**: Register members with durations (6 months, 1 year, 2 years).
- **Update Membership**: Placeholder for renewal or extension.
- **User Management**: Create new library user accounts.
- **View Logs**: View timestamped activity log of all actions (add book, issue, return, etc.).

### Common Features (Admin & Users)
- **Issue Book**:
  - Search by book name.
  - Auto-fetches author.
  - Decrements available count.
- **Return Book**:
  - Calculates fine if returned after 14-day loan period ($1/day).
  - Updates availability and logs return.
- **Check Book Availability**:
  - Quick lookup to see if a book is available.

---

## Database Schema

The system uses five SQLite tables:

1. **`users`**  
   - Stores user credentials: `id`, `username`, `password`

2. **`books`**  
   - Stores book details: `id`, `name`, `author`, `type` (book/movie), `quantity`, `available`

3. **`issued_books`**  
   - Tracks issued items: `book_id`, `username`, `issue_date`, `return_date`

4. **`memberships`**  
   - Member info: `member_name`, `duration`, `start_date`, `end_date`

5. **`logs`**  
   - Audit trail: `action`, `timestamp`

---

## Technical Details

- **GUI Framework**: `tkinter` (standard Python GUI library)
- **Database**: SQLite (`sqlite3` module)
- **Datetime Handling**: Uses `datetime` and `timedelta` for dates and overdue logic
- **UI/UX**:
  - Simple, clean layout with labels, entries, buttons, and radio buttons.
  - Scrollable log viewer using `Canvas` and `Scrollbar`.
  - Input validation and user feedback via `messagebox`.

---

## How to Run

1. Ensure Python 3.x is installed.
2. No external packages required (uses built-in modules).
3. Run the script:
   ```bash:disable-run
   python library_management.py
   ```
4. Login as:
   - **Admin**: `admin` / `admin123`
   - Or register a new user via admin panel.

---

## Limitations & Improvements

- **Security**: Passwords stored in plain text. Use hashing (e.g., `bcrypt`) in production.
- **Search**: Book lookup by name only (case-sensitive). Add fuzzy search or ID-based system.
- **Membership Integration**: Issuing books doesn't check membership status.
- **UI**: Basic design. Can be enhanced with `customtkinter` or themes.
- **Error Handling**: Minimal; can be expanded.
- **Export/Backup**: No data export (CSV/PDF) or backup feature.

---

## Use Cases

- Educational projects for learning OOP, GUI, and database integration.
- Prototype for small library or media rental systems.
- Foundation for extending into a full-featured library software.

---

## Future Enhancements

- Add search by author or genre.
- Email/SMS notifications for due dates.
- Generate reports (popular books, revenue from fines).
- Member dashboard with borrowing history.
- Barcode/QR support for book IDs.

---

**Developed with ❤️ using Python**  
*Note: This is a demo/educational project. Not intended for production without security upgrades.*
```
