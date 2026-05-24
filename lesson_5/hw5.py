"""Книжный магазин

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
count       INTEGER     DEFAULT 1                   Количество
price       FLOAT       NOT NULL, DEFAULT 0         Цена

Атрибут     Тип                 	                Описание
users       LIST[UserBookAssociation]               Список пользователей книги.
                                                    Связь многие-ко-многим

Добавьте следующие свойства:
- is_available - Получение информации о доступности/недоступности книги.
  Возвращает True/False. Книга доступна, если её количество > 0.

- list_users - Получение списка пользователей, у которых есть данная книга.
  Возвращает список строк в формате f'{user.id}: {user.fullname} ({user.name})'

Проверьте, что таблица создалась.

-------------------------------------------------------------------------------

Создайте таблицу users со следующей структурой:

Поле        Тип         Ограничения	                Описание
id	        INTEGER	    PRIMARY KEY AUTOINCREMENT	Уникальный идентификатор
name	    STRING(30)	NOT NULL, UNIQUE	        Ник пользователя
fullname	STRING(50)	                            ФИО пользователя

Атрибут     Тип                 	                Описание
books       LIST[UserBookAssociation]               Список книг пользователя.
                                                    Связь многие-ко-многим
delivery_info   LIST[Delivery]                      Список данных доставки
                                                    пользователя.
                                                    Связь один-ко-многим


Добавьте следующие свойства:
- is_books - Есть ли книги у пользователя. Возвращает True/False.

- list_books - Получение списка книг у пользователя.
  Возвращает список строк в формате f'{book.id}: {book.title} ({book.author})'

Проверьте, что таблица создалась.

-------------------------------------------------------------------------------

Создайте таблицу user_book_association со следующей структурой:

Поле        Тип         Ограничения	                Описание
user_id	    INTEGER	    PRIMARY KEY AUTOINCREMENT	Внешний ключ, ссылающийся
                                                    на users.id
book_id     INTEGER     PRIMARY KEY AUTOINCREMENT	Внешний ключ, ссылающийся
                                                    на books.id

Атрибут     Тип                 	                Описание
user        User                                    Связь с атрибутом books
book        Book                                    Связь с атрибутом users

Проверьте, что таблица создалась.

-------------------------------------------------------------------------------

Создайте таблицу delivery со следующей структурой:
Поле        Тип         Ограничения	                Описание
id	        INTEGER	    PRIMARY KEY AUTOINCREMENT	Уникальный идентификатор
user_id     INTEGER     FOREIGN KEY                 ID пользователя
email       STRING(50)  UNIQUE                      Почта пользователя
address     STRING                                  Адрес пользователя
phone       STRING(15)  UNIQUE                      Телефон пользователя

Атрибут     Тип                 	                Описание
user        User                                    Объект пользователя.
                                                    Связь многие-к-одному

Проверьте, что таблица создалась.

===============================================================================

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
        "count": 5,
        "price": 890.0
    },
    {
        "title": "Преступление и наказание",
        "author": "Федор Достоевский",
        "year": 1866,
        "isbn": "978-5-04-116633-9",
        "pages": 672,
        "genre": "Роман",
        "count": 3,
        "price": 750.0
    },
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
        "year": 1949,
        "isbn": "978-5-17-137262-4",
        "pages": 320,
        "genre": "Антиутопия",
        "count": 2,
        "price": 650.0
    },
    {
        "title": "Убить пересмешника",
        "author": "Харпер Ли",
        "year": 1960,
        "isbn": "978-5-04-116631-5",
        "pages": 416,
        "genre": "Роман",
        "count": 0,
        "price": 550.0
    },
    {
        "title": "Война и мир. Том 1",
        "author": "Лев Толстой",
        "year": 1867,
        "isbn": "978-5-17-135042-4",
        "pages": 720,
        "genre": "Роман-эпопея",
        "count": 1,
        "price": 1200.0
    },
    {
        "title": "Анна Каренина",
        "author": "Лев Толстой",
        "year": 1877,
        "isbn": "978-5-04-116632-2",
        "pages": 864,
        "genre": "Роман",
        "count": 0,
        "price": 950.0
    },
    {
        "title": "Собачье сердце",
        "author": "Михаил Булгаков",
        "year": 1925,
        "isbn": "978-5-17-135044-8",
        "pages": 352,
        "genre": "Повесть",
        "count": 4,
        "price": 590.0
    },
    {
        "title": "Маленький принц",
        "author": "Антуан де Сент-Экзюпери",
        "year": 1943,
        "isbn": "978-5-04-116634-6",
        "pages": 96,
        "genre": "Сказка",
        "count": 7,
        "price": 450.0
    },
    {
        "title": "Три товарища",
        "author": "Эрих Мария Ремарк",
        "year": 1936,
        "isbn": "978-5-17-137263-1",
        "pages": 384,
        "genre": "Роман",
        "count": 2,
        "price": 690.0
    },
    {
        "title": "Портрет Дориана Грея",
        "author": "Оскар Уайльд",
        "year": 1890,
        "isbn": "978-5-04-116635-3",
        "pages": 320,
        "genre": "Роман",
        "count": 0,
        "price": 520.0
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

-------------------------------------------------------------------------------

Добавьте в таблицу users следующих пользователей:
[
    {"name": "alice", "fullname": "Alice Wonderland"},
    {"name": "bob", "fullname": "Bob Builder"},
    {"name": "charlie", "fullname": "Charlie Brown"},
    {"name": "diana", "fullname": "Diana Princess"},
    {"name": "eve", "fullname": "Eve Smith"},
]

Требования:
- Используйте session.add_all().
- Выведите количество добавленных пользователей через длину списка объектов
  User.

-------------------------------------------------------------------------------

Добавьте в таблицу delivery следующие данные:
[
    {"user_id": 1, "email": "alice@example.com", "address": "Wonderland 1,
    London", "phone": "+79997776655"},
    {"user_id": 2, "email": "bob@example.com", "address": "Builder St 123,
    London", "phone": "+44-20-7946-0002"},
    {"user_id": 3, "email": None, "address": None, "phone": None},
    {"user_id": 4, "email": "diana@example.com", "address": "Princess Palace,
    London", "phone": None},
    {"user_id": 5, "email": None, "address": "Smith Lane 78, Dublin",
    "phone": "+353-1-234-5678"},
]

Требования:
- Используйте session.add_all().
- Выведите количество добавленных записей через длину списка объектов.

-------------------------------------------------------------------------------

Добавьте в таблицу user_book_association следующие данные:
[
    {"user_id": 1, "book_id": 1},
    {"user_id": 2, "book_id": 2},
    {"user_id": 3, "book_id": 3},
    {"user_id": 4, "book_id": 1},
    {"user_id": 1, "book_id": 2},
    {"user_id": 3, "book_id": 1},
    {"user_id": 3, "book_id": 10},
]

Требования:
- Используйте session.add_all().
- Выведите количество добавленных записей через длину списка объектов.

===============================================================================

3.Запросы:
- Найдите топ-3 самые популярные книги. Используйте limit(3), чтобы ограничить
  выборку.

- Выведите информацию в из таблиц в следующем виде:
  <Полное имя пользователя> (<Имя пользователя>):
      Купленные книги:
          <Название книги> - <Автор> (<Жанр>); <Цена> руб.
      Итого: <Общая сумма, потраченная пользователем на книги> руб.

  Пример:
  Alice Wonderland (alice):
    Купленные книги:
        Мастер и Маргарита - Михаил Булгаков (Роман); 890.0 руб.
        Преступление и наказание - Федор Достоевский (Роман); 750.0 руб.
    Итого: 1640.00 руб.

- Выведите пользователей, у кого нет хотя бы одного из полей: email, address,
  phone.

- Увеличьте цену всех книг на 5%. Верните через returning() названия книг и их
  новую цену. Выведите в формате
  <Название книги>: <Старая цена> -> <Новая цена> (<Разница>) руб.

- Сформируйте отчёт по магазину в формате:
```
1. Книги:
   - "1984": 2 шт. x 682.5 руб. = 1365.00 руб.
   - "Анна Каренина": 0 шт. x 997.5 руб. = 0.00 руб. (нет в наличии)
   - "Война и мир. Том 1": 1 шт. x 1260.0 руб. = 1260.00 руб.
   - "Маленький принц": 7 шт. x 472.5 руб. = 3307.50 руб.
   - "Мастер и Маргарита": 5 шт. x 934.5 руб. = 4672.50 руб.
   - "Портрет Дориана Грея": 0 шт. x 546.0 руб. = 0.00 руб. (нет в наличии)
   - "Преступление и наказание": 3 шт. x 787.5 руб. = 2362.50 руб.
   - "Собачье сердце": 4 шт. x 619.5 руб. = 2478.00 руб.
   - "Три товарища": 2 шт. x 724.5 руб. = 1449.00 руб.
   - "Убить пересмешника": 0 шт. x 577.5 руб. = 0.00 руб. (нет в наличии)

2. Активные читатели:
   - alice: 2 книга(и) (Мастер и Маргарита, Преступление и наказание)
   - bob: 1 книга(и) (Преступление и наказание)
   - charlie: 3 книга(и) (Мастер и Маргарита, 1984, Портрет Дориана Грея)
   - diana: 1 книга(и) (Мастер и Маргарита)

3. Самый популярный автор:
   - Михаил Булгаков (3 книга(и), 3 читатель(ей))
```

- Удалите пользователей без адреса. После удаления выведите удалённых
  пользователей, таблицу delivery, а также таблицу user_book_association.

- Удалите книгу с isbn=978-5-17-135043-1. После удаления выведите
  пользователей, которых затронуло удаление книги и таблицу
  user_book_association.

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

from sqlalchemy import (
    ForeignKey,
    String,
    create_engine,
    desc,
    distinct,
    func,
    or_,
    select,
    update,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

AVAILABLE = 1
NOT_AVAILABLE = 0

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
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int | None]
    isbn: Mapped[str | None] = mapped_column(unique=True)
    pages: Mapped[int] = mapped_column(default=0)
    genre: Mapped[str | None]
    count: Mapped[int] = mapped_column(default=1)
    price: Mapped[float] = mapped_column(default=0)
    users: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='book',
    cascade='all, delete, delete-orphan',)

    def __repr__(self):
        return (
            f'Book(id={self.id}, '
            f"title='{self.title}', "
            f"author='{self.author}', "
            f"year='{self.year}', "
            f"isbn='{self.isbn}', "
            f"pages='{self.pages}', "
            f"genre='{self.genre}', "
            f"count='{self.count}', "
            f"price='{self.price}')"
        )

    @property
    def is_available(self):
        return self.count > 0

    @property
    def list_users(self):
        return [f'{i.user.id}: {i.user.fullname} ({i.user.name})'
                for i in self.users]


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    fullname: Mapped[str | None] = mapped_column(String(50))
    books: Mapped[list['UserBookAssociation']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
    delivery_info: Mapped[list['Delivery']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )

    def __repr__(self):
        return (
            f'User(id={self.id}, '
            f"name='{self.name}', "
            f"fullname='{self.fullname}')"
        )

    @property
    def is_books(self):
        return len(self.books) > 0

    @property
    def list_books(self):
        return [f'{i.book.id}: {i.book.title} ({i.book.author})'
                for i in self.books]


class UserBookAssociation(Base):
    __tablename__ = 'user_book_association'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),
                                         primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'),
                                         primary_key=True)
    user: Mapped['User'] = relationship(back_populates='books')
    book: Mapped['Book'] = relationship(back_populates='users')

    def __repr__(self):
        return (
            f'UserBookAssociation(user_id={self.user_id}, '
            f'book_id={self.book_id})'
        )


class Delivery(Base):
    __tablename__ = 'delivery'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    email: Mapped[str | None] = mapped_column(String(50), unique=True)
    address: Mapped[str | None]
    phone: Mapped[str | None] = mapped_column(String(15), unique=True)
    user: Mapped['User'] = relationship(back_populates='delivery_info')

    def __repr__(self):
        return (
            f'Delivery(id={self.id}, '
            f'user_id={self.user_id}, '
            f"email='{self.email}', "
            f"address='{self.address}', "
            f"phone='{self.phone}')"
        )


class BookStore:
    def __init__(self, db_url='sqlite:///bookstore.db', echo=True):
        self.engine = create_engine(db_url, echo=echo)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def insert_books(self):
        books_data = [
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "year": 1967,
        "isbn": "978-5-17-135043-1",
        "pages": 480,
        "genre": "Роман",
        "count": 5,
        "price": 890.0
    },
    {
        "title": "Преступление и наказание",
        "author": "Федор Достоевский",
        "year": 1866,
        "isbn": "978-5-04-116633-9",
        "pages": 672,
        "genre": "Роман",
        "count": 3,
        "price": 750.0
    },
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
        "year": 1949,
        "isbn": "978-5-17-137262-4",
        "pages": 320,
        "genre": "Антиутопия",
        "count": 2,
        "price": 650.0
    },
    {
        "title": "Убить пересмешника",
        "author": "Харпер Ли",
        "year": 1960,
        "isbn": "978-5-04-116631-5",
        "pages": 416,
        "genre": "Роман",
        "count": 0,
        "price": 550.0
    },
    {
        "title": "Война и мир. Том 1",
        "author": "Лев Толстой",
        "year": 1867,
        "isbn": "978-5-17-135042-4",
        "pages": 720,
        "genre": "Роман-эпопея",
        "count": 1,
        "price": 1200.0
    },
    {
        "title": "Анна Каренина",
        "author": "Лев Толстой",
        "year": 1877,
        "isbn": "978-5-04-116632-2",
        "pages": 864,
        "genre": "Роман",
        "count": 0,
        "price": 950.0
    },
    {
        "title": "Собачье сердце",
        "author": "Михаил Булгаков",
        "year": 1925,
        "isbn": "978-5-17-135044-8",
        "pages": 352,
        "genre": "Повесть",
        "count": 4,
        "price": 590.0
    },
    {
        "title": "Маленький принц",
        "author": "Антуан де Сент-Экзюпери",
        "year": 1943,
        "isbn": "978-5-04-116634-6",
        "pages": 96,
        "genre": "Сказка",
        "count": 7,
        "price": 450.0
    },
    {
        "title": "Три товарища",
        "author": "Эрих Мария Ремарк",
        "year": 1936,
        "isbn": "978-5-17-137263-1",
        "pages": 384,
        "genre": "Роман",
        "count": 2,
        "price": 690.0
    },
    {
        "title": "Портрет Дориана Грея",
        "author": "Оскар Уайльд",
        "year": 1890,
        "isbn": "978-5-04-116635-3",
        "pages": 320,
        "genre": "Роман",
        "count": 0,
        "price": 520.0
    }
]

        with self.Session() as session:
            list_books = [Book(**data) for data in books_data]
            session.add_all(list_books)
            session.flush()
            len_id = len([book.id for book in list_books])
            session.commit()

            ResultHandler.add_section('2.1. Добавление книг')
            results.append(f'Добавлено книг: {len_id}')

    def insert_users(self):
        users_data = [
    {"name": "alice", "fullname": "Alice Wonderland"},
    {"name": "bob", "fullname": "Bob Builder"},
    {"name": "charlie", "fullname": "Charlie Brown"},
    {"name": "diana", "fullname": "Diana Princess"},
    {"name": "eve", "fullname": "Eve Smith"},
]

        with self.Session() as session:
            list_users = [User(**data) for data in users_data]
            session.add_all(list_users)
            session.commit()

            ResultHandler.add_section('2.2. Добавление пользователей')
            results.append(f'Добавлено пользователей: {len(list_users)}')

    def insert_delivery(self):
        delivery_data = [
    {"user_id": 1, "email": "alice@example.com",
     "address": "Wonderland 1, London", "phone": "+79997776655"},
    {"user_id": 2, "email": "bob@example.com",
     "address": "Builder St 123, London", "phone": "+44-20-7946-0002"},
    {"user_id": 3, "email": None, "address": None, "phone": None},
    {"user_id": 4, "email": "diana@example.com",
     "address": "Princess Palace, London", "phone": None},
    {"user_id": 5, "email": None, "address": "Smith Lane 78, Dublin",
     "phone": "+353-1-234-5678"},
]

        with self.Session() as session:
            list_delivery = [Delivery(**data) for data in delivery_data]
            session.add_all(list_delivery)
            session.commit()

            ResultHandler.add_section('2.3. Добавление данных доставки')
            results.append(f'Добавлено данных доставки: {len(list_delivery)}')

    def insert_user_book_association(self):
        book_association_data = [
    {"user_id": 1, "book_id": 1},
    {"user_id": 2, "book_id": 2},
    {"user_id": 3, "book_id": 3},
    {"user_id": 4, "book_id": 1},
    {"user_id": 1, "book_id": 2},
    {"user_id": 3, "book_id": 1},
    {"user_id": 3, "book_id": 10},
]

        with self.Session() as session:
            list_book_association = [UserBookAssociation(**data)
                                     for data in book_association_data]
            session.add_all(list_book_association)
            session.commit()

            ResultHandler.add_section(
                '2.4. Добавление данных ассоциации пользователя и книги'
            )
            results.append(f'Добавлено ассоциаций: '
                           f'{len(list_book_association)}')

    def get_top_books(self):
        with self.Session() as session:
            ResultHandler.add_section('3.1. Топ-3 самые популярные книги')
            stmt = (
                select(Book,
                       func.count(UserBookAssociation.book_id).label('cnt'))
                .join(UserBookAssociation,
                      Book.id == UserBookAssociation.book_id)
                .group_by(Book.id)
                .order_by(desc('cnt'))
                .limit(3)
            )
            top_3 = session.execute(stmt).all()
            for book, cnt in top_3:
                results.append(
                    f'{book} {cnt}')

    def get_user_purchases_report(self):
        with self.Session() as session:
            ResultHandler.add_section(
                '3.2. Информация о покупках пользователей')

            stmt = (
                select(User)
                .join(UserBookAssociation,
                      User.id == UserBookAssociation.user_id)
                .distinct()
                .order_by(User.id)
            )
            users = session.execute(stmt).scalars().all()

            for user in users:
                results.append(f'\n{user.fullname} ({user.name}):')
                results.append('    Купленные книги:')
                total = 0.0
                for i in sorted(user.books, key=lambda x: x.book_id):
                    results.append(f'        {i.book.title} - {i.book.author} '
                        f'({i.book.genre}); {i.book.price} руб.'
                    )
                    total += i.book.price
                results.append(f'    Итого: {total:.2f} руб.')

    def get_users_with_missing_delivery_data(self):
        with self.Session() as session:
            ResultHandler.add_section(
                '3.3. Пользователи с отсутствующими данными доставки')
            stmt = (
                select(User)
                .join(Delivery, User.id == Delivery.user_id)
                .where(
                    or_(
                        Delivery.email.is_(None),
                        Delivery.address.is_(None),
                        Delivery.phone.is_(None),
                    )
                )
                .order_by(User.id)
            )
            users = session.execute(stmt).scalars().all()
            for user in users:
                results.append(repr(user))

    def increase_prices_by_percent(self):
        with self.Session() as session:
            ResultHandler.add_section('3.4. Увеличение цены на 5%')
            old_books = session.execute(
                select(Book.id, Book.title, Book.price).order_by(Book.id)
            ).all()
            old_data = {row.id: (row.title, row.price) for row in old_books}
            stmt = (
                update(Book)
                .values(price=Book.price * 1.05)
                .returning(Book.id, Book.price)
            )
            updated_rows = session.execute(stmt).all()
            session.commit()

            for book_id, new_price in sorted(updated_rows, key=lambda r: r[0]):
                title, old_price = old_data[book_id]
                diff = new_price - old_price
                results.append(
                    f'{title}: {old_price:.2f} -> {new_price:.2f} '
                    f'({diff:.2f}) руб.'
                )

    def generate_store_report(self):
        with self.Session() as session:
            ResultHandler.add_section('3.5. Отчет по магазину')

            # ========== 1. Книги ==========
            results.append('\n1. Книги:')
            books = session.execute(
                select(Book).order_by(Book.title)
            ).scalars().all()
            for book in books:
                total = book.count * book.price
                line = (
                    f'   - "{book.title}": {book.count} шт. '
                    f'x {book.price} руб. = {total:.2f} руб.'
                )
                if not book.is_available:
                    line += ' (нет в наличии)'
                results.append(line)

            # ========== 2. Активные читатели ==========
            results.append('\n2. Активные читатели:')
            stmt = (
                select(User)
                .join(UserBookAssociation,
                      User.id == UserBookAssociation.user_id)
                .distinct()
                .order_by(User.name)
            )
            active_users = session.execute(stmt).scalars().all()

            for user in active_users:
                sorted_uba = sorted(user.books, key=lambda uba: uba.book_id)
                titles = [uba.book.title for uba in sorted_uba]
                results.append(
                    f'   - {user.name}: {len(titles)} книга(и) '
                    f'({", ".join(titles)})'
                )

            # ========== 3. Самый популярный автор ==========
            results.append('\n3. Самый популярный автор:')
            reader_count_col = func.count(
                distinct(UserBookAssociation.user_id)
            ).label('reader_count')
            stmt = (
                select(Book.author, reader_count_col)
                .join(UserBookAssociation,
                      Book.id == UserBookAssociation.book_id)
                .group_by(Book.author)
                .order_by(desc(reader_count_col))
                .limit(1)
            )
            row = session.execute(stmt).first()
            if row:
                author, reader_count = row
                results.append(f'   - {author} - {reader_count} читателя')

    def delete_users_without_address(self):
        with self.Session() as session:
            ResultHandler.add_section('3.6. Удаление пользователей без адреса')
            stmt = (
                select(User)
                .join(Delivery, User.id == Delivery.user_id)
                .where(Delivery.address.is_(None))
                .order_by(User.id)
            )
            users_to_delete = session.execute(stmt).scalars().all()

            results.append('Удалены пользователи: ')
            for user in users_to_delete:
                results.append(f'ID: {user.id}, Name: {user.name}')
                session.delete(user)

            session.commit()

            results.append('\nОставшиеся записи в таблице delivery:')
            deliveries = session.execute(
                select(Delivery).order_by(Delivery.id)
            ).scalars().all()
            for d in deliveries:
                results.append(f'  {repr(d)}')

            results.append(
                '\nОставшиеся записи в таблице user_book_association:'
            )
            assocs = session.execute(
                select(UserBookAssociation)
            ).scalars().all()
            for a in assocs:
                results.append(f'  {repr(a)}')

    def delete_book_by_isbn(self):
        with self.Session() as session:
            ResultHandler.add_section('3.7. Удаление книги по ISBN')
            book = session.execute(
                select(Book).where(Book.isbn == '978-5-17-135043-1')
            ).scalar_one()

            results.append('\nПользователи, у которых была эта книга:')
            for uba in book.users:
                user = uba.user
                results.append(f'  - {user.fullname} ({user.name})')

            session.delete(book)
            session.commit()

            results.append(
                '\nОставшиеся записи в таблице user_book_association:'
            )
            assocs = session.execute(
                select(UserBookAssociation)
            ).scalars().all()
            for a in assocs:
                user = session.get(User, a.user_id)
                b = session.get(Book, a.book_id)
                results.append(
                    f'  UserBookAssociation('
                    f'user_id={a.user_id} ({user.name}), '
                    f'book_id={a.book_id} ({b.title}))'
                )

    def run_all(self):
        self.create_tables()

        self.insert_books()
        self.insert_users()
        self.insert_delivery()
        self.insert_user_book_association()

        self.get_top_books()
        self.get_user_purchases_report()
        self.get_users_with_missing_delivery_data()
        self.increase_prices_by_percent()
        self.generate_store_report()
        self.delete_users_without_address()
        self.delete_book_by_isbn()

        print(*results, sep='\n')

        ResultHandler.save_results_to_file()

        ResultHandler.compare_results()


def main():
    bookstore = BookStore()
    bookstore.run_all()


if __name__ == '__main__':
    main()
