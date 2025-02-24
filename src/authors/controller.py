from flask import Blueprint
from .services import (add_author_service,get_author_by_id_service,
                       update_author_by_id_service, get_all_author_service,
                       delete_author_by_id_service, get_author_by_category_service)

authors = Blueprint("authors", __name__)

#add author
@authors.route("/managementBook/addAuthor", methods=['POST'])
def create_author():
    return add_author_service()

#get author by id
@authors.route("/managementBook/Author/<int:id>", methods=['GET'])
def get_author_by_id(id):
    return get_author_by_id_service(id)

#get all author
@authors.route("/managementBook/allAuthor", methods=['GET'])
def get_all_author():
    return get_all_author_service()

#update author by id
@authors.route("/managementBook/Author/<int:id>", methods=['PUT'])
def update_author_by_id(id):
    return update_author_by_id_service(id)

#delete author by id
@authors.route("/managementBook/Author/<int:id>", methods=['DELETE'])
def delete_book_by_id(id):
    return delete_author_by_id_service(id)

#get author by category
@authors.route("/managementBook/authorbyCategory/<category>", methods=['GET'])
def get_author_by_category(category):
    return get_author_by_category_service(category)