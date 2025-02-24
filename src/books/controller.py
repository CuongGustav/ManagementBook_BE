from flask import Flask, Blueprint
from .services import (add_book_service, get_book_by_id_service,
                       update_book_by_id_service, get_all_book_service,
                       delete_book_by_id_service, get_book_by_author_service,
                       get_book_by_category_service)

books = Blueprint("books", __name__)

#add book
@books.route("/managementBook/addBook", methods=['POST'])
def add_book():
    return add_book_service()

#get book by id
@books.route("/managementBook/Book/<int:id>", methods=['GET'])
def get_book_by_id(id):
    return get_book_by_id_service(id)

#get all book by id
@books.route("/managementBook/allBook", methods=['GET'])
def get_all_book():
    return get_all_book_service()

#update book by id
@books.route("/managementBook/Book/<int:id>", methods=['PUT'])
def update_book_by_id(id):
    return update_book_by_id_service(id)

#delete book by id
@books.route("/managementBook/Book/<int:id>", methods=['DELETE'])
def delete_book_by_id(id):
    return delete_book_by_id_service(id)

#get book by author
@books.route("/managementBook/bookByAuthor/<author>", methods=['GET'])
def get_book_by_author(author):
    return get_book_by_author_service(author)

#get book by category
@books.route("/managementBook/bookByCategory/<category>", methods=['GET'])
def get_book_by_category(category):
    return get_book_by_category_service(category)