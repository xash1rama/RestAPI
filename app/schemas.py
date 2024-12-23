from marshmallow import validates, post_load
from models import get_book_by_title, Book, Author
from python_advanced.module_17_rest_api.homework.app.models import get_author_by_id
from flasgger import Schema, fields, ValidationError

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Int(required=True)

    @validates('title')
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                'please use a different title.'.format(title=title)
            )
    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @validates("id")
    def validate_title(self, id: int) -> None:
        if get_author_by_id(id) is not None:
            raise ValidationError('Author with id "{id}" already exists'.format(id=id))

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        return Author(**data)

class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @validates("id")
    def validate_title(self, id: int) -> None:
        if get_author_by_id(id) is not None:
            raise ValidationError('Author with id "{id}" already exists'.format(id=id))

    @post_load
    def create_author(self, data: dict, **kwargs) -> Author:
        return Author(**data)
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)