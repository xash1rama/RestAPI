import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'A Byte of Python', "author":1},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', "author":2},
    {'id': 3, 'title': 'War and Peace', "author":3},
]
AUTHORS = [{"id": 1, "first_name": "Swaroop", "last_name": "Chip"},
           {"id": 2, "first_name": "Herman", "last_name": "Melville"},
           {"id": 3, "first_name": "Leo", "last_name": "Tolstoy"},
           {"id": 4, "first_name": "First", "last_name": "Toy"}]

ENABLE_FOREIGN_KEY = "PRAGMA foreign_keys = ON;"
DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = "authors"


@dataclass
class Book:
    title: str
    author: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)
@dataclass
class Author:
    first_name: str
    last_name: str
    id: Optional[int] = None
    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)

def init_db(initial_records_authors: List[Dict], initial_records_books) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{AUTHORS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {AUTHORS_TABLE_NAME}(id integer primary key autoincrement,
                    first_name varchar(50) not null ,
                    last_name varchar(50) not null);""")

            cursor.executemany(
                f"""
                        INSERT INTO authors
                        (first_name, last_name) VALUES (?, ?)
                        """,
                [
                    (item['first_name'], item['last_name'])
                    for item in initial_records_authors
                ]
            )
        cursor.execute(
            f"""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
                    """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"""
            CREATE TABLE {BOOKS_TABLE_NAME}
                (id integer primary key autoincrement,
                title varchar(50) not null,
                author integer not null references authors(id) ON DELETE CASCADE)""")

            cursor.executemany(f"""
            INSERT INTO {BOOKS_TABLE_NAME}(title, author) 
                VALUES (?, ?)""", [(item["title"], item["author"])
                                   for item in initial_records_books])





def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author=row[2])

def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2])


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]

def get_all_author_books(id) -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}` where author = ?', (id,))
        all_authors = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in all_authors]



def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
        f"""
                INSERT INTO `{BOOKS_TABLE_NAME}` 
                (title, author) VALUES (?, ?)
                """,
                (book.title, book.author)
            )
        book.id = cursor.lastrowid
        return book

def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
        f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}` 
                    (first_name, last_name) VALUES (?, ?)
                    """,
                    (author.first_name, author.last_name)
                )
        author.id = cursor.lastrowid
        return author



def get_author_by_id(author_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?
            """,
            (author_id,)
        )
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE id = ?
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()

def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME}
            WHERE id = ?
            """,
            (author_id,)
        )
        conn.commit()

def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM `{BOOKS_TABLE_NAME}` WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)

if __name__ == "__main__":
    init_db(AUTHORS, DATA)