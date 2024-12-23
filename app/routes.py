from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import APISpec, Swagger
from marshmallow import ValidationError
from apispec_webframeworks.flask import FlaskPlugin

from models import (
    DATA,
    AUTHORS,
    get_all_books,
    get_all_author_books,
    init_db,
    add_book,
    add_author
)
from python_advanced.module_17_rest_api.homework.app.models import get_book_by_id, delete_book_by_id, update_book_by_id, \
    delete_author_by_id
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)
spec = APISpec(title="BookList",
               version="1.0.0",
               openapi_version="2.0",
               plugins=[FlaskPlugin(), MarshmallowPlugin()])

class BookList(Resource):
    def post(self) -> tuple[dict, int]:
        """
        Endpoint для Добавления новой книги
        ---
        tags:
          - books
        parameters:
          - in: body
            name: book
            required: true
            schema:
              $ref: "#/definitions/Book"
        responses:
          201:
            description: "Книга успешно добавлена."
            schema:
              $ref: "#/definitions/Book"
          400:
            description: "Ошибка валидации данных."
            schema:
              type: object
              additionalProperties: true
        """
        data = request.json
        schema = BookSchema()

        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book = add_book(book)
        return schema.dump(book), 201

    def get(self):
        """
        Endpoint для полкчения всех книг
        ---
        tags:
          - books
        responses:
          200:
            description: "Book List."
            schema:
              type: array
              items:
                $ref: "#/definitions/Book"
        """
        schema = BookSchema()
        return schema.dump(get_all_books()), 200

class BookEdit(Resource):
    def get(self,id):
        """
        Endpoint для полкчения всех книг
        ---
        tags:
          - books/{id}
        parameters:
          - name: id
            in: path
            required: true
            type: integer
            description: "ID книги."
        responses:
          200:
            description: "Информация о книге."
            schema:
              $ref: "#/definitions/Book"
            """
        schema = BookSchema()
        return schema.dump(get_book_by_id(id)), 200

    def put(self,id):
        """
        Endpoint для обновления данных книги по ID
        ---
        tags:
          - books/{id}
        parameters:
          - name: id
            in: path
            required: true
            type: integer
            description: "ID книги."
          - in: body
            name: book
            required: true
            schema:
              $ref: "#/definitions/Book"
        responses:
          201:
            description: "Книга успешно обновлена."
            schema:
              $ref: "#/definitions/Book"
          400:
            description: "Ошибка валидации данных."
        """
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        book.id = id
        update_book_by_id(book,)
        return schema.dump(book), 201

    def delete(self, id):
        """
        Endpoint для удаления книги по ID
        ---
        tags:
          - books/{id}
        parameters:
          - name: id
            in: path
            required: true
            type: integer
            description: "ID книги."
        responses:
          200:
            description: "Книга успешно удалена."
            schema:
              $ref: "#/definitions/Book"
        """
        schema = BookSchema()
        return schema.dump(delete_book_by_id(id)), 200


class AuthorList(Resource):
    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201

class AuthorEdit(Resource):
    def get(self, id):
        schema = AuthorSchema()
        return schema.dump(get_all_author_books(id), many=True), 200

    def delete(self, id) :
        schema = AuthorSchema()
        author = delete_author_by_id(id)
        if author:
            return schema.dump(author), 200
        return {'message': 'Author not find'}, 404

templates = spec.to_flasgger(app,
                             definitions=[BookSchema, AuthorSchema],
                             )
swagger = Swagger(app, template=templates, template_file="swagger.json")

api.add_resource(BookList, '/api/books')
api.add_resource(BookEdit, '/api/books/<int:id>')

api.add_resource(AuthorList,  '/api/authors')
api.add_resource(AuthorEdit,  '/api/authors/<int:id>')

if __name__ == '__main__':
    init_db(initial_records_books=DATA, initial_records_authors=AUTHORS)
    app.run(debug=True)
