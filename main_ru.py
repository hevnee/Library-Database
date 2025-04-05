import sqlite3

database = sqlite3.connect("library.db")
cursor = database.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NULL,
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
        [("петр алешковский", "Москва, РСФСР, СССР"),
        ("виктор астафьев", "Овсянка, Енисейская губерния, РСФСР"),
        ("михаил бутов", "Москва, Россия"),
        ("георгий владимов", "Харьков, СССР"),
        ("владимир маканин", "Орск, Оренбургская область, РСФСР, СССР"),
        ("ирина полянская", "Касли Челябинской области")])
    cursor.executemany("INSERT OR IGNORE INTO books (title, author_id, year, pages) VALUES (?, ?, ?, ?)", 
        [("жизнеописание хорька", 1, 2011, 288),
        ("так хочется жить", 2, 1996, 448),
        ("свобода", 3, 2002, 264),
        ("генерал и его армия", 4, 1997, 576),
        ("андеграунд, или герой нашего времени", 5, 2003, 480),
        ("прохождение тени", 6, 1999, 448)])
    database.commit()

def new_author():
    print("\n[ Добавление автора ]")
    author_name = str(input("Имя автора: ")).lower()
    if cursor.execute("SELECT name FROM authors WHERE name = ?", (author_name,)).fetchone() is None:
        author_country = str(input("Место рождения автора: ")).lower()
        cursor.execute("INSERT OR IGNORE INTO authors (name, country) VALUES (?, ?)", 
            (author_name, author_country))
        database.commit()
        print("Автор добавлен в базу.")
    else:
        print("Этот автор уже есть в системе.")
        return

def new_book():
    print("\n[ Добавление книги ]")
    author_id = str(input("Имя автора: ")).lower()
    fetchone_id = cursor.execute("SELECT id FROM authors WHERE name = ?", (author_id,)).fetchone()
    if fetchone_id is None:
        print("Автор не найден.")
    else:
        title = str(input("Название книги: ")).lower()
        cursor.execute("SELECT title FROM books WHERE title = ? AND author_id = ?", (title, int(fetchone_id[0])))
        if cursor.fetchone() is None:
            year = int(input("Год издания: "))
            pages = int(input("Количество страниц: "))
            cursor.execute("INSERT OR IGNORE INTO books (title, author_id, year, pages) VALUES (?, ?, ?, ?)", 
                (title, int(fetchone_id[0]), year, pages))
            database.commit()
            print("Книга успешно добавлена.")
        else:
            print("Эта книга уже есть у данного автора.")
            return

def search():
    print("\n[ Поиск книг автора ]")
    result = []
    author_name = str(input("Имя автора: ")).lower()
    cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
    check_author_name = cursor.fetchone()
    if check_author_name is None:
        print("Автор не найден.")
        return
    else:
        cursor.execute("SELECT title FROM books WHERE author_id = ?", (check_author_name[0],))
        titles = cursor.fetchall()
        for i in titles:
            result.append(f'"{i[0]}"')
        print(f"Книги автора {author_name.title()}: {', '.join(result)}.")

def array_count():
    print("\n[ Список авторов и их книг ]")
    cursor.execute("SELECT id, name FROM authors")
    authors = cursor.fetchall()    
    for i in range(len(authors)):
        aiO = authors[i][1]
        cursor.execute("SELECT COUNT(title) FROM books WHERE author_id = ?", (authors[i][0],))
        count_books = cursor.fetchall()
        print(f"Автор: {aiO.title()} | Книг: {count_books[0][0]}")

def delete_book():
    print("\n[ Удаление книги ]")
    title = str(input("Название книги: ")).lower()
    cursor.execute("SELECT author_id FROM books WHERE title = ?", (title,))
    authors_id = cursor.fetchall()
    if not authors_id:
        print("Книга не найдена.")
        return
    else:
        names = []
        for i in range(len(authors_id)):
            cursor.execute("SELECT name FROM authors WHERE id = ?", (authors_id[i][0],))
            names.append(cursor.fetchone()[0].title())
        author_name = str(input(f"Выберите автора: {', '.join(names)}\nАвтор: ")).lower()
        cursor.execute("SELECT name, id FROM authors WHERE name = ?", (author_name,))
        check_author_name = cursor.fetchone()
        if check_author_name is None:
            print("Автор не найден.")
            return
        else:
            r_u_s = str(input("Подтвердите удаление [y/n]: ")).lower()
            if r_u_s == "y":
                cursor.execute("DELETE FROM books WHERE title = ? AND author_id = (SELECT id FROM authors WHERE name = ?)", (title, author_name))
                database.commit()
                print("Книга удалена.")
            else:
                print("Удаление отменено.")
                return

def update_year():
    print("\n[ Изменение года издания ]")
    title = str(input("Название книги: ")).lower()
    cursor.execute("SELECT author_id FROM books WHERE title = ?", (title,))
    authors_id = cursor.fetchall()
    if not authors_id:
        print("Книга не найдена.")
        return
    else:
        names = []
        for i in range(len(authors_id)):
            cursor.execute("SELECT name FROM authors WHERE id = ?", (authors_id[i][0],))
            names.append(cursor.fetchone()[0].title())
        author_name = str(input(f"Выберите автора: {', '.join(names)}\nАвтор: ")).lower()
        cursor.execute("SELECT name, id FROM authors WHERE name = ?", (author_name,))
        check_author_name = cursor.fetchone()
        if check_author_name is None:
            print("Автор не найден.")
            return
        else:
            year = int(input(f'Новый год издания для "{title}": '))
            cursor.execute("UPDATE books SET year = ? WHERE title = ? AND author_id = ?", (year, title, check_author_name[1]))
            database.commit()
            print(f'Год издания книги "{title}" обновлён.')

create_tables()

while True:
    print("""=== Библиотечная система ===
        1. Добавить автора
        2. Добавить книгу
        3. Найти книги автора
        4. Список авторов
        5. Удалить книгу
        6. Изменить год издания
        7. Выход""")
    variant = int(input("Выберите действие: "))
    if variant == 1: new_author()
    elif variant == 2: new_book()
    elif variant == 3: search()
    elif variant == 4: array_count()
    elif variant == 5: delete_book()
    elif variant == 6: update_year()
    elif variant == 7: print("Работа завершена."); break
    else: print("Неверный ввод.")

database.commit()
database.close()
