from flask import Blueprint, render_template, request, jsonify
from helpers import token_required
from models import  db, Book, book_schema, books_schema

books = Blueprint('books', __name__, url_prefix='/api')

@books.route('/books', methods= ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    ISBN = request.json['ISBN']
    pages = request.json['pages']
    back_cover = request.json['back_cover']
    user_token = current_user_token.token

    new_book = Book(title, author, ISBN, pages, back_cover, user_token = user_token)

    db.session.add(new_book)
    db.session.commit()

    response = book_schema.dump(new_book)
    return jsonify(response)

@books.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@books.route('/books/<id>', methods = ['GET'])
@token_required
def get_individual_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

@books.route('/books/<id>', methods =['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.title = request.json['title']
    book.author = request.json['author']
    book.ISBN = request.json['ISBN']
    book.pages = request.json['pages']
    book.back_cover = request.json['back_cover']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@books.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)
