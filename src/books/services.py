from flask import request, jsonify
from src.extension import db
from src.library_ma import BookSchema
from src.model import Books, Author, Category
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# add book
def add_book_service():
    data = request.get_json()
    if (data and ('name' in data) and ('page_count' in data)
            and ('author_id' in data) and ('category_id' in data)):
        name = data['name']
        page_count = data['page_count']
        author_id = data['author_id']
        category_id = data['category_id']
        try:
            new_book = Books(name, page_count, author_id, category_id)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({"message": "Add success!"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Failed to update book!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Request error"}), 400
    
#get book by id
def get_book_by_id_service(id):
    book = Books.query.get(id)
    if book:
        return book_schema.jsonify(book), 200
    else:
        return jsonify({"message": "Not found book"}), 404
    
#get all book
def get_all_book_service():
    books = Books.query.all()
    if books:
        return books_schema.jsonify(books), 200  
    else:
        return jsonify({"message": "Not get all book"}), 404


#update book by id
def update_book_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        return jsonify({"message": "Book not found!"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"mesage": "Invalid JSON data"}), 400
    
    try:
        editable_fields = {'name', 'page_count', 'categpry_id', 'author_id'}
        for key, value in data.items():
            if key in editable_fields:
                setattr(book, key, value)
        db.session.commit()
        return jsonify({"message": "Book updated successfully!"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update book!", "error": str(e)}), 500
    

#delete book by id
def delete_book_by_id_service(id):
    book = Books.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "delete book complete"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete book!", "error": str(e)}), 500
    
#get book by author and view author.name, category
def get_book_by_author_service(author):
    if not author or not isinstance(author, str):
        return jsonify({"message": "Invalid author name"}), 400
    try:
        books = db.session.query(Books.id, Books.name, Books.page_count, Author.name.label('author_name'),
                                Category.name.label('category_name')) \
            .join(Author, Books.author_id == Author.id) \
            .join(Category, Books.category_id == Category.id) \
            .filter(func.lower(Author.name) == author.lower()) \
            .all()
        
        if books:
            return jsonify([{
                "id": book.id,
                "name": book.name,
                "page_count": book.page_count,
                "author": book.author_name,
                "category": book.category_name
            } for book in books]), 200
        else:
            return jsonify({"message": f"No books found by author {author}"}), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error occurred", "error": str(e)}), 500
    
#get book by category
def get_book_by_category_service(category):
    if not category or not isinstance(category, str):
        return jsonify({"message": "Invalid category name"}), 400
    try:
        books = db.session.query(Books.id, Books.name, Books.page_count, Author.name.label('author_name'),
                                 Category.name.label('category_name'))\
            .join(Author, Books.author_id == Author.id)\
            .join(Category, Books.category_id == Category.id)\
            .filter(func.lower(Category.name) == func.lower(category))\
            .all()
        
        if books:
            return jsonify([{
                "id": book.id,
                "name": book.name,
                "page_count": book.page_count,
                "author_name": book.author_name,
                "category_name": book.category_name
            } for book in books]), 200
        else:
            return jsonify({"message": f"No books found by category {category}"}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error occurred", "error": str(e)}), 500




#get book by author
# def get_book_by_author_service(author):
#     if not author or not isinstance(author, str):
#         return jsonify({"message": "Invalid author name"}), 400
    
#     try:
#         books = Books.query.join(Author).filter(
#             func.lower(Author.name) == author.lower()
#         ).all()
#         if books:
#             return  books_schema.jsonify(books), 200
#         else:
#             return jsonify({"message": f"Not found books by {author}"}), 404
#     except SQLAlchemyError as e:
#         return jsonify({"message": "Database error occurred", "error": str(e)}), 500
