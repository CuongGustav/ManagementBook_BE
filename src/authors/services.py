from flask import jsonify, request
from src.extension import db
from src.library_ma import AuthorSchema
from src.model import Author, Category, Books
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

# add author
def add_author_service():
    data = request.get_json()
    if (data and ('name' in data)):
        name = data['name']
        try:
            new_author = Author(name)
            db.session.add(new_author)
            db.session.commit()
            return jsonify({"message" : "Add success"}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update book!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Request Error"}), 400  

# get author by id
def get_author_by_id_service(id):
    author = Author.query.get(id)
    if (author): 
        return author_schema.jsonify(author), 200
    else:
        return jsonify({"message": "Cannot find author"}), 404

#get all author
def get_all_author_service():
    authors = Author.query.all()
    if authors:
        return authors_schema.jsonify(authors), 200
    else:
        return jsonify({"message": "Cannot get all author "})

#update author by id
def update_author_by_id_service(id):
    author = Author.query.get(id)
    if not author:
        return jsonify({"message": "Author not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON data"}), 400
    
    try:
        editable_fileds ={"name"}
        for key, value in data.items():
            if key in editable_fileds:
                setattr(author, key, value)
        db.session.commit()
        return jsonify({"mesage": "Update Author Complete"}), 200
    except SQLAlchemyError as e:
        db.session.rollback
        return jsonify({"message": "Failed to update Author!", "error": str(e)}), 500
    
#delete auhtor by id
def delete_author_by_id_service (id):
    author = Author.query.get(id)
    if not author:
        return jsonify({"message": "Cannot Found Author"}), 404
    try:
        db.session.delete(author)
        db.session.commit()
        return jsonify({"message": "Delete Author Complete"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete Author", "error": str(e)}), 500
    
#get author by category
def get_author_by_category_service (category):
    if not category or not isinstance( category, str):
        return jsonify({"mesage": "Invalid category name"}), 400
    try:
        authors = db.session.query(Author.id, Author.name)\
            .join(Books, Author.id ==  Books.author_id )\
            .join(Category, Books.category_id == Category.id)\
            .filter (func.lower(Category.name) == func.lower(category)).all()
        if authors:
            return ([{
                "id": author.id,
                "anme": author.name
            } for author in authors]), 200
        else:
            return jsonify({"message": "Cannot found author by category"}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Failed to found author by category ", "error": str(e)}),500

