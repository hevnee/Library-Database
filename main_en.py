import sqlite3

database = sqlite3.connect("library.db")
cursor = database.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT,
            UNIQUE (name)
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER REFERENCES authors(id),
            year INTEGER,
            pages INTEGER,
            UNIQUE (title, author_id)
        )""")
    cursor.executemany("INSERT OR IGNORE INTO authors (name, country) VALUES (?, ?)", 
        [("George Orwell", "United Kingdom"),
        ("J.K. Rowling", "United Kingdom"),
        ("Ernest Hemingway", "United States"),
        ("Agatha Christie", "United Kingdom"),
        ("Mark Twain", "United States"),
        ("Jane Austen", "United Kingdom")])
    cursor.executemany("INSERT OR IGNORE INTO books (title, author_id, year, pages) VALUES (?, ?, ?, ?)", 
        [("1984", 1, 1949, 328),
        ("harry potter and the philosopher's stone", 2, 1997, 223),
        ("the old man and the sea", 3, 1952, 127),
        ("murder on the orient express", 4, 1934, 256),
        ("the adventures of tom sawyer", 5, 1876, 274),
        ("pride and prejudice", 6, 1813, 279)])
    database.commit()

def new_author():
    print("\n[ Add New Author ]")
    author_name = str(input("Author's name: ")).title()
    if cursor.execute("SELECT name FROM authors WHERE name = ?", (author_name,)).fetchone() is None:
        author_country = str(input("Author's country: ")).lower()
        cursor.execute("INSERT OR IGNORE INTO authors (name, country) VALUES (?, ?)", 
            (author_name, author_country))
        database.commit()
        print("Author added successfully.")
    else:
        print("This author already exists in the database.")
        return

def new_book():
    print("\n[ Add New Book ]")
    author_name = str(input("Author's name: ")).title()
    fetchone_id = cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,)).fetchone()
    if fetchone_id is None:
        print("Author not found.")
    else:
        title = str(input("Book title: ")).lower()
        cursor.execute("SELECT title FROM books WHERE title = ? AND author_id = ?", (title, int(fetchone_id[0])))
        if cursor.fetchone() is None:
            year = int(input("Year of publication: "))
            pages = int(input("Number of pages: "))
            cursor.execute("INSERT OR IGNORE INTO books (title, author_id, year, pages) VALUES (?, ?, ?, ?)", 
                (title, int(fetchone_id[0]), year, pages))
            database.commit()
            print("Book added successfully.")
        else:
            print("This book by the author already exists.")
            return

def search():
    print("\n[ Search Books by Author ]")
    result = []
    author_name = str(input("Author's name: ")).title()
    cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
    check_author_name = cursor.fetchone()
    if check_author_name is None:
        print("Author not found.")
        return
    else:
        cursor.execute("SELECT title FROM books WHERE author_id = ?", (check_author_name[0],))
        titles = cursor.fetchall()
        for i in titles:
            result.append(f'"{i[0]}"')
        print(f"Books by {author_name()}: {', '.join(result)}.")

def array_count():
    print("\n[ Authors and Their Book Count ]")
    cursor.execute("SELECT id, name FROM authors")
    authors = cursor.fetchall()
    for i in range(len(authors)):
        aiO = authors[i][1]
        cursor.execute("SELECT COUNT(title) FROM books WHERE author_id = ?", (authors[i][0],))
        count_books = cursor.fetchall()
        print(f"Author: {aiO} | Books: {count_books[0][0]}")
 
def delete_book():
    print("\n[ Delete a Book ]")
    title = str(input("Название книги: ")).lower()
    cursor.execute("SELECT author_id FROM books WHERE title = ?", (title,))
    authors_id = cursor.fetchall()
    if not authors_id:
        print("Book not found.")
        return
    else:
        names = []
        for i in range(len(authors_id)):
            cursor.execute("SELECT name FROM authors WHERE id = ?", (authors_id[i][0],))
            names.append(cursor.fetchone()[0])
        author_name = str(input(f"Select author: {', '.join(names)}\nAuthor: ")).title()
        cursor.execute("SELECT name, id FROM authors WHERE name = ?", (author_name,))
        check_author_name = cursor.fetchone()
        if check_author_name is None:
            print("Author not found in the list.")
            return
        else:
            r_u_s = str(input("Confirm deletion [y/n]: ")).lower()
            if r_u_s == "y":
                cursor.execute("DELETE FROM books WHERE title = ? AND author_id = (SELECT id FROM authors WHERE name = ?)", (title, author_name))
                database.commit()
                print("Book deleted successfully.")
            else:
                print("Deletion cancelled.")
                return

def update_year():
    print("\n[ Update Publication Year ]")
    title = str(input("Book title: ")).lower()
    cursor.execute("SELECT author_id FROM books WHERE title = ?", (title,))
    authors_id = cursor.fetchall()
    if not authors_id:
        print("Book not found.")
        return
    else:
        names = []
        for i in range(len(authors_id)):
            cursor.execute("SELECT name FROM authors WHERE id = ?", (authors_id[i][0],))
            names.append(cursor.fetchone()[0])
        author_name = str(input(f"Select author: {', '.join(names)}\nAuthor: ")).title()
        cursor.execute("SELECT name, id FROM authors WHERE name = ?", (author_name,))
        check_author_name = cursor.fetchone()
        if check_author_name is None:
            print("Author not found in the list.")
            return
        else:
            year = int(input(f'New publication year for "{title}": '))
            cursor.execute("UPDATE books SET year = ? WHERE title = ? AND author_id = ?", (year, title, check_author_name[1]))
            database.commit()
            print(f'Publication year for "{title}" updated to {year}.')

create_tables()

while True:
    print("""=== Library Management System ===
        1. Add Author
        2. Add Book
        3. Search Books by Author
        4. List Authors and Book Count
        5. Delete Book
        6. Update Publication Year
        7. Exit""")
    variant = int(input("Select an option: "))
    if variant == 1: new_author()
    elif variant == 2: new_book()
    elif variant == 3: search()
    elif variant == 4: array_count()
    elif variant == 5: delete_book()
    elif variant == 6: update_year()
    elif variant == 7: print("Exiting the system. Goodbye!"); break
    else: print("Invalid input. Please try again.")

database.commit()
database.close()
