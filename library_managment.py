import mysql.connector
from datetime import date

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost" ,
    user= "root" ,
    password= "shaury2016" ,
    database="library_db"
)

cursor = db.cursor()

# Add Book
def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    qty = int(input("Enter quantity: "))

    sql = "INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (title, author, qty))
    db.commit()
    print("Book added successfully!")

# Show Books
def show_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    print("\n--- Book List ---")
    for b in books:
        print(b)

# Issue Book
def issue_book():
    book_id = int(input("Enter book ID to issue: "))
    name = input("Enter student name: ")

    # Check quantity
    cursor.execute("SELECT quantity FROM books WHERE book_id=%s", (book_id,))
    result = cursor.fetchone()

    if result and result[0] > 0:
        sql = "INSERT INTO issued_books (book_id, student_name, issue_date) VALUES (%s,%s,%s)"
        cursor.execute(sql, (book_id, name, date.today()))

        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE book_id=%s", (book_id,))
        db.commit()
        print("Book issued successfully!")
    else:
        print("Book not available!")

# Return Book
def return_book():
    issue_id = int(input("Enter issue ID to return: "))

    cursor.execute("SELECT book_id FROM issued_books WHERE issue_id=%s", (issue_id,))
    result = cursor.fetchone()

    if result:
        book_id = result[0]

        cursor.execute("DELETE FROM issued_books WHERE issue_id=%s", (issue_id,))
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE book_id=%s", (book_id,))
        db.commit()
        print("Book returned successfully!")
    else:
        print("Invalid issue ID")

# Main Menu
while True:
    print("\n===== Library Management System =====")
    print("1. Add Book")
    print("2. Show Books")
    print("3. Issue Book")
    print("4. Return Book")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        show_books()
    elif choice == "3":
        issue_book()
    elif choice == "4":
        return_book()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice")