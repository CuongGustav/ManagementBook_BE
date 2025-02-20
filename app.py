from flask import Flask, request, jsonify
from models import db, Book
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
CORS(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Get all books
@app.route("/books", methods=["GET"])
def get_books():
    try: 
        books = Book.query.all()
        return jsonify([book.to_dict() for book in books]), 200
    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500

# Add new book
@app.route("/books", methods=["POST"])
def add_book():
    try:
        data = request.json
        if not data or not all(key in data for key in ["title", "author", "year"]):
            return jsonify({"message": "Missing data"}), 400
        new_book = Book (
            title=data["title"],
            author=data["author"],
            year = data["year"]
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify(new_book.to_dict()), 201
    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500

# Update book by ID
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        data = request.json
        if not data:
            return jsonify({"message": "Missing data"}), 400
        book.title = data.get("title", book.title)
        book.author = data.get("author", book.author)
        book.year = data.get("year", book.year)

        db.session.commit()
        return jsonify(book.to_dict()),200
    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500
    

# Delete book by ID
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted"}), 200
    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500

# Get book details by ID
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_detail(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict()), 200
    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)