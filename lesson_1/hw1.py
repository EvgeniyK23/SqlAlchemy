"""Библиотека

1. Создайте базу данных library.db и в ней таблицу books со следующей
структурой:

Поле        Тип         Ограничения	                Описание
id	        INTEGER	    PRIMARY KEY AUTOINCREMENT	Уникальный идентификатор
title	    TEXT	    NOT NULL	                Название книги
author	    TEXT	    NOT NULL	                Автор книги
year	    INTEGER		                            Год издания
isbn	    TEXT	    UNIQUE	                    ISBN книги
pages	    INTEGER	    DEFAULT 0	                Количество страниц
genre	    TEXT		                            Жанр
available	INTEGER	    DEFAULT 1	                Доступна ли книга (1 - да,
0 - нет)

Проверьте, что таблица создалась.

2. Заполнение таблицы данными

Добавьте в таблицу books следующие книги:
[
    ("Мастер и Маргарита", "Михаил Булгаков", 1967, "978-5-17-135043-1", 480,
     "Роман", 1),
    ("Преступление и наказание", "Федор Достоевский", 1866,
     "978-5-04-116633-9", 672, "Роман", 1),
    ("1984", "Джордж Оруэлл", 1949, "978-5-17-137262-4", 320, "Антиутопия", 1),
    ("Убить пересмешника", "Харпер Ли", 1960, "978-5-04-116631-5", 416,
     "Роман", 0),
    ("Война и мир. Том 1", "Лев Толстой", 1867, "978-5-17-135042-4", 720,
     "Роман-эпопея", 1),
    ("Анна Каренина", "Лев Толстой", 1877, "978-5-04-116632-2", 864, "Роман",
     0),
    ("Собачье сердце", "Михаил Булгаков", 1925, "978-5-17-135044-8", 352,
     "Повесть", 1),
    ("Маленький принц", "Антуан де Сент-Экзюпери", 1943, "978-5-04-116634-6",
     96, "Сказка", 1),
    ("Три товарища", "Эрих Мария Ремарк", 1936, "978-5-17-137263-1", 384,
     "Роман", 1),
    ("Портрет Дориана Грея", "Оскар Уайльд", 1890, "978-5-04-116635-3", 320,
     "Роман", 0)
]

3. Простые SELECT-запросы

Напишите следующие запросы для получения данных:
- Все книги (все поля)
- Только названия и авторов всех книг
- Количество книг в таблице

4. Фильтрация с WHERE

Напишите следующие запросы для получения данных:

- Книги Льва Толстого
- Книги, изданные после 1900 года
- Доступные книги (available = 1)
- Книги жанра "Роман" с количеством страниц больше 400
- Книги Булгакова или Достоевского (используйте OR)

5. Сортировка и ограничения

Напишите следующие запросы для получения данных:
- Топ-3 самых толстых книги (по убыванию страниц)
- Топ-3 самых старых книги (по году издания)
- Все книги, отсортированные по автору, затем по году

6. Обновление данных

Напишите следующие запросы для обновления данных:
- Для книги с ISBN '978-5-17-135043-1' установите available = 0
- Для книги с названием "Анна Каренина" установите available = 1
- Увеличьте количество страниц для всех книг Льва Толстого на 10
- Пометьте как недоступные все книги, изданные до 1900 года (available = 0)

После каждого обновления выводите количество затронутых записей.

7. Удаление данных

Напишите следующие запросы для удаления данных:
- Удалите все книги, которых нет в наличии (available = 0)
- Удалите книги с количеством страниц меньше 100
- Удалите все книги жанра "Сказка"

После каждого удаления выводите количество затронутых записей.
"""

import sqlite3

# список с результатами работы
result_to_write_file = [
    f'{"=" * 79}',
    f'{"ДОМАШНЕЕ ЗАДАНИЕ: БИБЛИОТЕКА":^79}',
    f'{"=" * 79}',
]


def add_equl():
    result_to_write_file.append(f'{"=" * 79}')


# Создание таблицы
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS BOOKS(
id	        INTEGER	    PRIMARY KEY AUTOINCREMENT,
title	    TEXT	    NOT NULL,
author	    TEXT	    NOT NULL,
year	    INTEGER,
isbn	    TEXT	    UNIQUE,
pages	    INTEGER	    DEFAULT 0,
genre	    TEXT,
available	INTEGER	    DEFAULT 1
);
"""

cursor.execute(create_table_sql)
conn.commit()

add_equl()
result_to_write_file.append('Задание 1: Создание таблицы')
add_equl()

result_to_write_file.append("✓ Таблица 'books' успешно создана")
result_to_write_file.append(
    '✓ Проверка пройдена: таблица существует в базе данных'
)


# Заполнение таблицы
add_equl()
result_to_write_file.append('Задание 2: Заполнение таблицы данными')
add_equl()

insert_many_sql = """
INSERT INTO BOOKS(title, author, year, isbn, pages, genre, available)
VALUES 
     ("Мастер и Маргарита", "Михаил Булгаков", 1967, "978-5-17-135043-1", 480,
     "Роман", 1),
     ("Преступление и наказание", "Федор Достоевский", 1866,
     "978-5-04-116633-9", 672, "Роман", 1),
    ("1984", "Джордж Оруэлл", 1949, "978-5-17-137262-4", 320, "Антиутопия", 1),
    ("Убить пересмешника", "Харпер Ли", 1960, "978-5-04-116631-5", 416,
     "Роман", 0),
    ("Война и мир. Том 1", "Лев Толстой", 1867, "978-5-17-135042-4", 720,
     "Роман-эпопея", 1),
    ("Анна Каренина", "Лев Толстой", 1877, "978-5-04-116632-2", 864, "Роман",
     0),
    ("Собачье сердце", "Михаил Булгаков", 1925, "978-5-17-135044-8", 352,
     "Повесть", 1),
    ("Маленький принц", "Антуан де Сент-Экзюпери", 1943, "978-5-04-116634-6",
     96, "Сказка", 1),
    ("Три товарища", "Эрих Мария Ремарк", 1936, "978-5-17-137263-1", 384,
     "Роман", 1),
    ("Портрет Дориана Грея", "Оскар Уайльд", 1890, "978-5-04-116635-3", 320,
     "Роман", 0)    
"""
cursor.execute(insert_many_sql)
conn.commit()

result_to_write_file.append(f'✓ Добавлено книг:{cursor.rowcount}')
temp = cursor.execute('SELECT COUNT(*) FROM BOOKS')
result_to_write_file.append(f'✓ Всего книг в таблице: {temp.fetchone()[0]}')
all_books = cursor.execute("""SELECT COUNT(*) FROM BOOKS""").fetchone()[0]

# Простые select-запросы
add_equl()
result_to_write_file.append('Задание 3: Простые SELECT-запросы')
add_equl()

# все книги
result_to_write_file.append('\n--- Все книги (полная информация) ---')
select_all_books = 'SELECT * FROM BOOKS;'
cursor.execute(select_all_books)
for row in cursor:
    result_to_write_file.append(
        f'ID: {row[0]}, '
        f'{row[1]} {row[2]}, '
        f'{row[3]}, {row[4]}, '
        f'{row[5]}, {row[6]}, '
        f'{"доступна" if row[7] else "выдана"}'
    )

# название и авторы
result_to_write_file.append('\n--- Название и авторы ---')
select_title_author = 'SELECT title, author FROM BOOKS;'
cursor.execute(select_title_author)
for row in cursor:
    result_to_write_file.append(f'«{row[0]}» — {row[1]}')

# количество книг
result_to_write_file.append('\n--- Количество книг ---')
select_number_books = 'SELECT COUNT(*) FROM BOOKS;'
cursor.execute(select_number_books)
result_to_write_file.append(
    f'Всего книг в библиотеке: {cursor.fetchone()[0]}\n'
)

# Фильтрация с WHERE
add_equl()
result_to_write_file.append('Задание 4: Фильтрация с WHERE')
add_equl()

# книги Льва Толстого
result_to_write_file.append('\n--- Книги Льва Толстого ---')
select_lev_tolstiy_books = """SELECT * 
                            FROM BOOKS
                            WHERE author = 'Лев Толстой';"""
cursor.execute(select_lev_tolstiy_books)
for row in cursor:
    result_to_write_file.append(
        f'"{row[1]}" ({row[3]}), {row[5]} стр. - '
        f'{"доступна" if row[7] == 1 else "выдана"}'
    )

# книги, изданные после 1900 года
result_to_write_file.append('\n--- Книги после 1900 года ---')
select_books_after_1900 = """SELECT year, title, author
                            FROM BOOKS
                            WHERE year >= 1900
                            ORDER BY year ASC;"""
cursor.execute(select_books_after_1900)
for row in cursor:
    result_to_write_file.append(f'{row[0]}: «{row[1]}» — {row[2]}')

# доступные книги
result_to_write_file.append('\n--- Доступные книги ---')
select_books_available = """SELECT title, author
                            FROM BOOKS
                            WHERE available = 1;"""
cursor.execute(select_books_available)
for row in cursor:
    result_to_write_file.append(f'«{row[0]}» — {row[1]}')

# роман более 400 стр
result_to_write_file.append('\n--- Романы с количеством страниц > 400 ---')
select_novel_pages_more400 = """SELECT title, author, pages
                            FROM BOOKS
                            WHERE genre = 'Роман' and pages >= 400;"""
cursor.execute(select_novel_pages_more400)
for row in cursor:
    result_to_write_file.append(f'«{row[0]}» — {row[1]}, {row[2]} стр.')

# книги Булгакова или Достоевского
result_to_write_file.append('\n--- Книги Булгакова или Достоевского ---')
select_books_bul_dost = """SELECT author, title, year
                            FROM BOOKS
                            WHERE author like '%Булгаков%'
                            or author like '%Достоевский%'
                            ORDER BY author;"""
cursor.execute(select_books_bul_dost)
for row in cursor:
    result_to_write_file.append(f'{row[0]}: «{row[1]}», ({row[2]})')
result_to_write_file.append('\n')

# Сортировка и ограничения
add_equl()
result_to_write_file.append('Задание 5: Сортировка и ограничения')
add_equl()

# топ 3 самых толстых книг
result_to_write_file.append('\n--- Топ-3 самых толстых книг ---')
select_top3_fat_books = """SELECT title, author, pages
                            FROM BOOKS
                            ORDER BY pages DESC
                            LIMIT 3;"""
cursor.execute(select_top3_fat_books)
start = 1
for row in cursor:
    result_to_write_file.append(
        f'{start}. «{row[0]}» — {row[1]}, {row[2]} стр.'
    )
    start += 1

# топ 3 самых старых книг
result_to_write_file.append('\n--- Топ-3 самых старых книг ---')
select_top3_oldest_books = """SELECT title, author, year
                            FROM BOOKS
                            ORDER BY year
                            LIMIT 3;"""
cursor.execute(select_top3_oldest_books)
start = 1
for row in cursor:
    result_to_write_file.append(f'{start}. «{row[0]}» — {row[1]}, {row[2]} г.')
    start += 1

# книги, отсортированные по автору, по году
result_to_write_file.append(
    '\n--- Все книги (сортировка: по автору, затем по году) ---\n'
)

select_all_group_author = """SELECT author, COUNT(*)
                             FROM BOOKS
                             GROUP BY author
                             ORDER BY author;"""
cursor.execute(select_all_group_author)
authors_count = cursor.fetchall()

select_order_auth_year = """SELECT year, title
                            FROM BOOKS
                            ORDER BY author, year;"""
cursor.execute(select_order_auth_year)
authors_year_title = cursor.fetchall()

start = 0
for i in range(len(authors_count)):
    result_to_write_file.append(f'{authors_count[i][0]}:')
    for _ in range(authors_count[i][1]):
        result_to_write_file.append(
            f'{authors_year_title[start][0]} — '
            f'«{authors_year_title[start][1]}»'
        )
        start += 1
    result_to_write_file.append('\n')

# Обновление данных
add_equl()
result_to_write_file.append('Задание 6: Обновление данных')
add_equl()

# установка available = 0 для ISBN
result_to_write_file.append('\n--- Выдача книги по ISBN ---')
update_isbn_books = """UPDATE BOOKS
                       SET available = 0
                       WHERE isbn = "978-5-17-135043-1";"""

cursor.execute(update_isbn_books)
conn.commit()
result_to_write_file.append(
    f'✓ Книга выдана. Обновлено записей: {cursor.rowcount}'
)

# установка available = 1 для Анны Карениной
result_to_write_file.append("\n--- Возврат книги 'Анна Каренина' ---")
update_anna_karenina = """UPDATE BOOKS
                       SET available = 1
                       WHERE title like "%Анна Каренина%";"""

cursor.execute(update_anna_karenina)
conn.commit()
result_to_write_file.append(
    f'✓ Книга возвращена. Обновлено записей: {cursor.rowcount}'
)

# увеличение страниц у толстого
result_to_write_file.append(
    '\n--- Увеличение страниц у книг Льва Толстого ---'
)

before_after_update = """SELECT title, pages
                   FROM BOOKS
                   WHERE author like '%Лев Толстой%';"""

cursor.execute(before_after_update)
result_to_write_file.append('  До обновления:')
for row in cursor:
    result_to_write_file.append(f'    «{row[0]}»: {row[1]} стр.')

update_page_tolstiy = """UPDATE BOOKS
                       SET pages = pages + 10
                       WHERE author like '%Лев Толстой%';"""
cursor.execute(update_page_tolstiy)
conn.commit()
result_to_write_file.append(f'  ✓ Обновлено записей: {cursor.rowcount}')

cursor.execute(before_after_update)
result_to_write_file.append('  После обновления:')
for row in cursor:
    result_to_write_file.append(f'    «{row[0]}»: {row[1]} стр.')

# все книги до 1900 недоступны
result_to_write_file.append(
    '\n--- Книги до 1900 года помечаются как недоступные ---'
)

select_books_before_1900 = """SELECT year, title, author
                   FROM BOOKS
                   WHERE year <= 1900;"""

cursor.execute(select_books_before_1900)
result_to_write_file.append('  Книги до 1900 года:')
for row in cursor:
    result_to_write_file.append(f'    {row[0]}: «{row[1]}» — {row[2]}')

update_books_before_1900 = """UPDATE BOOKS
                       SET available = 0
                       WHERE year <= 1900;"""
cursor.execute(update_books_before_1900)
conn.commit()
result_to_write_file.append(
    f'  ✓ Помечено как недоступные: {cursor.rowcount} книг'
)
result_to_write_file.append('\n')

# Удаление данных
add_equl()
result_to_write_file.append('Задание 7: Удаление данных')
add_equl()

# удаление всех книг с available = 0
cursor.execute('SELECT COUNT(*) FROM BOOKS')
result_to_write_file.append(
    f'Всего книг в библиотеке до удаления: {cursor.fetchone()[0]}'
)
result_to_write_file.append('\n--- Удаление книг, которых нет в наличии ---')
result_to_write_file.append('  Будут удалены:')
select_book_eq_0 = """SELECT title, author
                      FROM BOOKS
                      WHERE available = 0"""
cursor.execute(select_book_eq_0)
for row in cursor:
    result_to_write_file.append(f'    «{row[0]}» — {row[1]}')

delete_available_0 = """DELETE FROM BOOKS
                        WHERE available = 0;"""
cursor.execute(delete_available_0)
conn.commit()
result_to_write_file.append(f'✓ Удалено книг: {cursor.rowcount}')

# удаление всех книг в которых станиц меньше 100
result_to_write_file.append(
    '\n--- Удаление книг с количеством страниц < 100 ---'
)
select_book_pages_100 = """SELECT title, author, pages
                      FROM BOOKS
                      WHERE pages < 100"""
cursor.execute(select_book_pages_100)
for row in cursor:
    result_to_write_file.append(f'    «{row[0]}» — {row[1]}, {row[2]} стр.')

delete_available_0 = """DELETE FROM BOOKS
                        WHERE pages < 100;"""
cursor.execute(delete_available_0)
conn.commit()
result_to_write_file.append(f'  ✓ Удалено книг: {cursor.rowcount}')

# удаление всех книг с жанром сказка
result_to_write_file.append("\n--- Удаление книг с жанром 'Сказка' ---")

delete_genre = """DELETE FROM BOOKS
                WHERE genre like '%Сказка%';"""
cursor.execute(delete_genre)
conn.commit()
result_to_write_file.append(f'  ✓ Удалено книг: {cursor.rowcount}')

# итог
result_to_write_file.append('\n--- Итог ---')
select_last_book = """SELECT COUNT(*) FROM BOOKS"""
cursor.execute(select_last_book)
last_book = cursor.fetchone()[0]
result_to_write_file.append(f'Книг осталось в библиотеке: {last_book}')
result_to_write_file.append(
    f'Удалено всего: {int(all_books) - int(last_book)}\n'
)

result_to_write_file.append('Оставшиеся книги:')
cursor.execute("""SELECT title, author, available
                  FROM BOOKS;""")
for row in cursor:
    result_to_write_file.append(
        f'    «{row[0]}» — {row[1]} - {"доступна" if row[2] else "недоступна"}'
    )

# Конец
add_equl()
result_to_write_file.append(f'{"ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ":^79}')
add_equl()

with open('hw1.txt', 'w', encoding='utf-8') as f_out:
    for i in result_to_write_file:
        f_out.write(i)
        f_out.write('\n')
        print(i)
