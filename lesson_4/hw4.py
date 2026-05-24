"""Библиотека с книгами и пользователями

❗Данную домашнюю работу выполнять, используя SQLAlchemy ORM и Session!

1. Создайте базу данных bookstore.db

Book и User - названия классов.

Создайте таблицу Book со следующей структурой:

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

Создайте таблицу User со следующей структурой:
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
- Используйте session.add_all(list_books) для добавления данных в сеанс, где
  list_books - список объектов Book.
- Получите id добавляемых книг с помощью метода flush().
- Выведите количество добавленных книг, как длина полученного списка id книг.

Подсказки:
- Для генерации списка объектов из словаря можно использовать следующую
  конструкцию: books = [Book(**data) for data in books_data], где books_data -
  список словарей.

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
- Используйте session.add_all().
- id книг соответствуют номерам элементов из списка книг
- Выведите количество добавленных пользователей через длину списка объектов
  User.

3. SELECT-запросы

Напишите следующие запросы для получения данных:
- Все книги (все поля)
- Все пользователи (все поля)
- Доступные книги (available = 1)
- Книги, авторы (author) которых имеют букву "э" в названии
- Доступные книги, год которых меньше 1900
- Ник пользователя (name) и ФИО пользователя (fullname)
- Ник пользователя, ФИО пользователя, Название книги (title) (join можно
  использовать также, как и раньше.

В качестве проверки используйте файл с выводом результатов запросов
(result.txt).
Формат вывода результата запросов можно посмотреть в этом же файле.

*Для очищения таблиц при тестировании используйте следующий код:
Base.metadata.drop_all(engine)

Составьте свой файлик с ответом 'my_result.txt' и запишите в него свои
результаты с помощью функции save_results_to_file.
Сравните содержимое файликов с помощью вызова функции compare_results.
"""

import os

from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

results = []


class ResultHandler:
    @staticmethod
    def add_section(title):
        results.append('\n' + '=' * 10 + title + '=' * 10)

    @staticmethod
    def save_results_to_file(filename='my_result.txt'):
        with open(filename, 'w', encoding='utf-8') as f:
            for line in results:
                f.write(line + '\n')

    @staticmethod
    def compare_results(my_file='my_result.txt', expected_file='result.txt'):
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

        if differences:
            print('❌ НАЙДЕНЫ РАЗЛИЧИЯ:')
            for diff in differences:
                print(diff)

            assert False, f'Найдено {len(differences)} различий с эталоном'  # noqa
        else:
            print('✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!')
            return True


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = 'Book'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int | None]
    isbn: Mapped[str | None]
    pages: Mapped[int] = mapped_column(default=0)
    genre: Mapped[str | None]
    available: Mapped[int] = mapped_column(default=1)

    def __repr__(self):
        return (
            f'Book(id={self.id}, '
            f"title='{self.title}', "
            f"author='{self.author}', "
            f'year={self.year!r}, '
            f'isbn={self.isbn!r}, '
            f'pages={self.pages!r}, '
            f'genre={self.genre!r}, '
            f'available={self.available!r})'
        )


class User(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None] = mapped_column(String(50))
    book_id: Mapped[int] = mapped_column(ForeignKey('Book.id'))

    def __repr__(self):
        return (
            f'User(id={self.id}, '
            f"name='{self.name}', "
            f"fullname='{self.fullname}', "
            f'book_id={self.book_id})'
        )


class LibraryORM:
    def __init__(self, db_url='sqlite:///bookstore.db', echo=True):
        self.engine = create_engine(db_url, echo=echo)  # TODO: создание движка
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        # TODO: здесь должно быть удаление таблиц и их создание через metadata
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def insert_books(self):
        books_data = [
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
        list_books = [Book(**data) for data in books_data]

        with self.Session() as session:
            session.add_all(list_books)
            session.flush()
            id = [book.id for book in list_books]
            session.commit()

            ResultHandler.add_section('2.1. Добавление книг')
            results.append(f'Добавлено книг: {len(id)}')

    def insert_users(self):
        users_data = [
            {'name': 'alice', 'fullname': 'Alice Wonderland', 'book_id': 1},
            {'name': 'bob', 'fullname': 'Bob Builder', 'book_id': 3},
            {'name': 'charlie', 'fullname': 'Charlie Brown', 'book_id': 2},
            {'name': 'diana', 'fullname': 'Diana Princess', 'book_id': 7},
            {'name': 'eve', 'fullname': 'Eve Smith', 'book_id': 5},
        ]
        list_users = [User(**data) for data in users_data]

        with self.Session() as session:
            session.add_all(list_users)
            session.commit()

            ResultHandler.add_section('2.2. Добавление пользователей')
            results.append(f'Добавлено пользователей: {len(list_users)}')

    def execute_queries(self):
        with self.Session() as session:
            ResultHandler.add_section('3.1. Все книги (все поля)')
            stmt = select(Book)
            result = session.execute(stmt).scalars().all()
            for i in result:
                results.append(str(i))

            ResultHandler.add_section('3.2. Все пользователи (все поля)')
            result = session.execute(select(User)).scalars().all()
            for i in result:
                results.append(str(i))

            ResultHandler.add_section('3.3. Доступные книги (available = 1)')
            stmt = select(Book).where(Book.available == 1)
            result = session.execute(stmt).scalars().all()
            for i in result:
                results.append(str(i))

            ResultHandler.add_section(
                "3.4. Книги, авторы которых имеют букву 'э'"
            )
            stmt = select(Book).where(Book.author.contains('э'))
            result = session.execute(stmt).scalars().all()
            for i in result:
                results.append(str(i))

            ResultHandler.add_section(
                '3.5. Доступные книги, год которых меньше 1900'
            )
            stmt = select(Book).where(
                (Book.year < 1900) & (Book.available == 1)
            )
            result = session.execute(stmt).scalars().all()
            for i in result:
                results.append(str(i))

            ResultHandler.add_section('3.6. Ник и ФИО пользователей')
            result = session.execute(select(User.name, User.fullname)).all()
            for i in result:
                results.append(f'{i[0]}: {i[1]}')

            ResultHandler.add_section('3.7. Пользователи и их книги')
            stmt = select(User.name, User.fullname, Book.title).join(
                Book, isouter=True
            )
            result = session.execute(stmt).all()
            for i in result:
                results.append(f'{i[0]} ({i[1]}): {i[2]}')

    def run_all(self):
        self.create_tables()

        self.insert_books()
        self.insert_users()

        self.execute_queries()

        print(*results, sep='\n')

        ResultHandler.save_results_to_file()

        ResultHandler.compare_results()


def main():
    library = LibraryORM()
    library.run_all()


if __name__ == '__main__':
    main()
