"""Библиотека с книгами и пользователями

1. Создайте базу данных bookstore.db

Создайте таблицу books со следующей структурой:

Поле        Тип         Ограничения	                Описание
id	        INTEGER	    PRIMARY KEY AUTOINCREMENT	Уникальный идентификатор
title	    STRING	    NOT NULL	                Название книги
author	    STRING	    NOT NULL	                Автор книги
year	    INTEGER		                            Год издания
isbn	    STRING	    UNIQUE	                    ISBN книги
pages	    INTEGER	    DEFAULT 0	                Количество страниц
genre	    STRING		                            Жанр
available	INTEGER	    DEFAULT 1	                Доступна ли книга (1 - да,
0 - нет)

Проверьте, что таблица создалась.

Создайте таблицу users со следующей структурой:
Поле        Тип         Ограничения	                Описание
id	        INTEGER	    PRIMARY KEY AUTOINCREMENT	Уникальный идентификатор
name	    STRING(30)	NOT NULL, UNIQUE	        Ник пользователя
fullname	STRING(50)	                            ФИО пользователя
book_id     INTEGER     FOREIGN KEY, NOT NULL       ID взятой книги

Проверьте, что таблица создалась.

2. Заполнение таблиц данными

Добавьте в таблицу books следующие книги:
[
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "year": 1967,
        "isbn": "978-5-17-135043-1",
        "pages": 480,
        "genre": "Роман",
        "available": 1
    },
    {
        "title": "Преступление и наказание",
        "author": "Федор Достоевский",
        "year": 1866,
        "isbn": "978-5-04-116633-9",
        "pages": 672,
        "genre": "Роман",
        "available": 1
    },
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
        "year": 1949,
        "isbn": "978-5-17-137262-4",
        "pages": 320,
        "genre": "Антиутопия",
        "available": 1
    },
    {
        "title": "Убить пересмешника",
        "author": "Харпер Ли",
        "year": 1960,
        "isbn": "978-5-04-116631-5",
        "pages": 416,
        "genre": "Роман",
        "available": 0
    },
    {
        "title": "Война и мир. Том 1",
        "author": "Лев Толстой",
        "year": 1867,
        "isbn": "978-5-17-135042-4",
        "pages": 720,
        "genre": "Роман-эпопея",
        "available": 1
    },
    {
        "title": "Анна Каренина",
        "author": "Лев Толстой",
        "year": 1877,
        "isbn": "978-5-04-116632-2",
        "pages": 864,
        "genre": "Роман",
        "available": 0
    },
    {
        "title": "Собачье сердце",
        "author": "Михаил Булгаков",
        "year": 1925,
        "isbn": "978-5-17-135044-8",
        "pages": 352,
        "genre": "Повесть",
        "available": 1
    },
    {
        "title": "Маленький принц",
        "author": "Антуан де Сент-Экзюпери",
        "year": 1943,
        "isbn": "978-5-04-116634-6",
        "pages": 96,
        "genre": "Сказка",
        "available": 1
    },
    {
        "title": "Три товарища",
        "author": "Эрих Мария Ремарк",
        "year": 1936,
        "isbn": "978-5-17-137263-1",
        "pages": 384,
        "genre": "Роман",
        "available": 1
    },
    {
        "title": "Портрет Дориана Грея",
        "author": "Оскар Уайльд",
        "year": 1890,
        "isbn": "978-5-04-116635-3",
        "pages": 320,
        "genre": "Роман",
        "available": 0
    }
]

Требования:
- Используйте insert() с множественной вставкой и возвратом ID (returning())
- Выведите количество добавленных книг, как длина полученного списка id книг

Добавьте в таблицу users следующие данные:
[
    {
        "name": "alice",
        "fullname": "Alice Wonderland",
        "book_id": 1
    },
    {
        "name": "bob",
        "fullname": "Bob Builder",
        "book_id": 3
    },
    {
        "name": "charlie",
        "fullname": "Charlie Brown",
        "book_id": 2
    },
    {
        "name": "diana",
        "fullname": "Diana Princess",
        "book_id": 7
    },
    {
        "name": "eve",
        "fullname": "Eve Smith",
        "book_id": 5
    }
]

Требования:
- Используйте insert() с множественной вставкой
- id книг соответствуют номерам элементов из списка книг
- Выведите количество добавленных пользователей с помощью result.rowcount, где
result - результат запроса в БД

3. SELECT-запросы

Напишите следующие запросы для получения данных:
- Все книги (все поля)
- Все пользователи (все поля)
- Доступные книги (available = 1)
- Книги, авторы (author) которых имеют букву "э" в названии
- Доступные книги, год которых меньше 1900
- Ник пользователя (name) и ФИО пользователя (fullname)
* Ник пользователя, ФИО пользователя, Название книги (title) (необязательный
запрос, так как JOIN мы еще не проходили).

В качестве проверки используйте файл с выводом результатов запросов
(result.txt).
Формат вывода результата запросов можно посмотреть в этом же файле.

*Для очищения таблиц при тестировании используйте следующий код перед insert:
conn.execute(books.delete()) и conn.execute(users.delete())

Составьте свой файлик с ответом 'my_result.txt' и запишите в него свои
результаты с помощью функции save_results_to_file.
Сравните содержимое файликов с помощью вызова функции compare_results.

Если дополнительный запрос не реализован - удалите его результат из файла
result.txt
"""

import os

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
    insert,
    select,
)

results = []


def save_results_to_file(filename: str = 'my_result.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for line in results:
            f.write(line + '\n')


def compare_results(
    my_file: str = 'my_result.txt', expected_file: str = 'result.txt'
):
    print('\n' + '=' * 60)
    print('🔍 СРАВНЕНИЕ РЕЗУЛЬТАТОВ С ЭТАЛОНОМ')
    print('=' * 60)

    if not os.path.exists(expected_file):
        print(f'⚠️  Эталонный файл {expected_file} не найден.')
        print('   Создайте его вручную или скопируйте от преподавателя.')
        print('   Пропускаю сравнение...')
        return False

    if not os.path.exists(my_file):
        print(f'❌ Файл с моими результатами {my_file} не найден!')
        return False

    with open(my_file, 'r', encoding='utf-8') as f:
        my_lines = [line.rstrip() for line in f.readlines()]

    with open(expected_file, 'r', encoding='utf-8') as f:
        expected_lines = [line.rstrip() for line in f.readlines()]

    assert len(my_lines) == len(expected_lines), (
        f'Разное количество строк: моих {len(my_lines)}, эталон '
        f'{len(expected_lines)}'
    )

    differences = []
    for i, (my_line, expected_line) in enumerate(
        zip(my_lines, expected_lines)  # noqa
    ):
        if my_line != expected_line:
            differences.append(
                f'Строка {i + 1}:\n  '
                f'Моя:     {my_line}\n  Эталон:  {expected_line}'
            )

    # Если есть различия, выводим их и вызываем assert
    if differences:
        print('❌ НАЙДЕНЫ РАЗЛИЧИЯ:')
        for diff in differences:
            print(diff)

        assert False, f'Найдено {len(differences)} различий с эталоном'  # noqa
    else:
        print('✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!')
        return True


def add_section(title: str):
    results.append('\n' + '=' * 10 + title + '=' * 10)


def create_tables(engine, metadata):
    """Задание 1: Создание таблиц books и users"""
    books_table = Table(
        'books',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String, nullable=False),
        Column('author', String, nullable=False),
        Column('year', Integer),
        Column('isbn', String, unique=True),
        Column('pages', Integer, default=0),
        Column('genre', String),
        Column('available', Integer, default=1),
    )

    users_table = Table(
        'users',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(30), nullable=False, unique=True),
        Column('fullname', String(50)),
        Column('book_id', Integer, ForeignKey('books.id'), nullable=False),
    )

    metadata.create_all(engine)

    return books_table, users_table


def insert_books(engine, data_books, books_table):
    """Задание 2.1: Добавление книг"""

    with engine.connect() as conn:
        conn.execute(books_table.delete())
        conn.commit()

    with engine.connect() as con:
        stmt = (
            insert(books_table).values(data_books).returning(books_table.c.id)
        )
        result = con.execute(stmt)
        add_section('2.1. Добавление книг')
        results.append(f'Добавлено книг: {len(result.all())}')
        con.commit()


def insert_users(engine, data_users, users_table):
    """Задание 2.2: Добавление пользователей"""

    with engine.connect() as conn:
        conn.execute(users_table.delete())
        conn.commit()

    with engine.connect() as con:
        result = con.execute(insert(users_table).values(data_users))
        add_section('2.2. Добавление пользователей')
        results.append(f'Добавлено пользователей: {result.rowcount}')
        con.commit()


def execute_queries(engine, books_table, users_table):
    """Задание 3: SELECT-запросы"""

    with engine.connect() as con:
        add_section('3.1. Все книги (все поля)')
        stmt = select(books_table)
        result = con.execute(stmt).fetchall()
        for i in result:
            results.append(str(i))

        add_section('3.2. Все пользователи (все поля)')
        stmt = select(users_table)
        result = con.execute(stmt).fetchall()
        for i in result:
            results.append(str(i))

        add_section('3.3. Доступные книги (available = 1)')
        stmt = select(books_table).where(books_table.c.available == 1)
        result = con.execute(stmt).fetchall()
        for i in result:
            results.append(str(i))

        add_section("3.4. Авторы с буквой 'э'")
        stmt = select(books_table).where(
            func.lower(books_table.c.author).contains('э')
        )
        result = con.execute(stmt).fetchall()
        for i in result:
            results.append(str(i))

        add_section('3.5. Доступные книги, год которых меньше 1900')
        stmt = select(books_table).where(
            (books_table.c.year < 1900) & (books_table.c.available == 1)
        )
        result = con.execute(stmt).fetchall()
        for i in result:
            results.append(str(i))

        add_section('3.6. Ник и ФИО пользователей')
        stmt = select(users_table.c.name, users_table.c.fullname)
        result = con.execute(stmt).fetchall()
        for i in result:
            results.append(f'{i.name}: {i.fullname}')

        # 3.7 * (необязательный)
        add_section('3.7. * Пользователи и их книги (с JOIN)')
        stmt = select(
            users_table.c.name,
            users_table.c.fullname,
            books_table.c.title,
            books_table.c.author,
        ).select_from(
            users_table.join(
                books_table, users_table.c.book_id == books_table.c.id
            )
        )
        result = con.execute(stmt).fetchall()
        for i in result:
            results.append(
                f"{i.name}: ({i.fullname}) -> '{i.title}' - {i.author}"
            )


def main():
    # Создаем движок и метаданные
    engine = create_engine('sqlite:///bookstore.db', echo=True)

    metadata = MetaData()

    # Создание таблиц
    books, users = create_tables(engine, metadata)

    # Вставка книг
    data_books = [
        {
            'title': 'Мастер и Маргарита',
            'author': 'Михаил Булгаков',
            'year': 1967,
            'isbn': '978-5-17-135043-1',
            'pages': 480,
            'genre': 'Роман',
            'available': 1,
        },
        {
            'title': 'Преступление и наказание',
            'author': 'Федор Достоевский',
            'year': 1866,
            'isbn': '978-5-04-116633-9',
            'pages': 672,
            'genre': 'Роман',
            'available': 1,
        },
        {
            'title': '1984',
            'author': 'Джордж Оруэлл',
            'year': 1949,
            'isbn': '978-5-17-137262-4',
            'pages': 320,
            'genre': 'Антиутопия',
            'available': 1,
        },
        {
            'title': 'Убить пересмешника',
            'author': 'Харпер Ли',
            'year': 1960,
            'isbn': '978-5-04-116631-5',
            'pages': 416,
            'genre': 'Роман',
            'available': 0,
        },
        {
            'title': 'Война и мир. Том 1',
            'author': 'Лев Толстой',
            'year': 1867,
            'isbn': '978-5-17-135042-4',
            'pages': 720,
            'genre': 'Роман-эпопея',
            'available': 1,
        },
        {
            'title': 'Анна Каренина',
            'author': 'Лев Толстой',
            'year': 1877,
            'isbn': '978-5-04-116632-2',
            'pages': 864,
            'genre': 'Роман',
            'available': 0,
        },
        {
            'title': 'Собачье сердце',
            'author': 'Михаил Булгаков',
            'year': 1925,
            'isbn': '978-5-17-135044-8',
            'pages': 352,
            'genre': 'Повесть',
            'available': 1,
        },
        {
            'title': 'Маленький принц',
            'author': 'Антуан де Сент-Экзюпери',
            'year': 1943,
            'isbn': '978-5-04-116634-6',
            'pages': 96,
            'genre': 'Сказка',
            'available': 1,
        },
        {
            'title': 'Три товарища',
            'author': 'Эрих Мария Ремарк',
            'year': 1936,
            'isbn': '978-5-17-137263-1',
            'pages': 384,
            'genre': 'Роман',
            'available': 1,
        },
        {
            'title': 'Портрет Дориана Грея',
            'author': 'Оскар Уайльд',
            'year': 1890,
            'isbn': '978-5-04-116635-3',
            'pages': 320,
            'genre': 'Роман',
            'available': 0,
        },
    ]

    insert_books(engine, data_books, books)

    # Вставка пользователей
    data_users = [
        {'name': 'alice', 'fullname': 'Alice Wonderland', 'book_id': 1},
        {'name': 'bob', 'fullname': 'Bob Builder', 'book_id': 3},
        {'name': 'charlie', 'fullname': 'Charlie Brown', 'book_id': 2},
        {'name': 'diana', 'fullname': 'Diana Princess', 'book_id': 7},
        {'name': 'eve', 'fullname': 'Eve Smith', 'book_id': 5},
    ]

    insert_users(engine, data_users, users)

    # Выполнение запросов
    execute_queries(engine, books, users)

    # Вывод результатов
    print(*results, sep='\n')

    # Сохранение в файл
    save_results_to_file()

    # Сравнение результатов
    compare_results()


if __name__ == '__main__':
    main()
