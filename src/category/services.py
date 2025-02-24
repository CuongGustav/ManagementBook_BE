from flask import request, jsonify
from src.extension import db
from src.model import Category
from src.library_ma import CatSchema
from sqlalchemy.exc import SQLAlchemyError

category_schema = CatSchema()
categorys_schema = CatSchema( many = True)

#add category
def add_category_service():
    data = request.get_json()
    if (data and ('name' in data)):
        name = data['name']
        try:
            new_category = Category(name)
            db.session.add(new_category)
            db.session.commit()
            return jsonify ({"mesage": "Create Success"}), 201
        except SQLAlchemyError as e:
            return jsonify ({"message": "Can not add book", "error": str(e)}), 500    
    else:
        return jsonify ({'message': "Request Error"}), 400
    
#get category by id
def get_category_by_id_service(id):
    category = Category.query.get(id)
    if (category):
        return category_schema.jsonify(category), 200
    else:
        return jsonify ({'message': "Request Error"}), 400
    
#get all category
def get_all_category_service():
    categories = Category.query.all()
    if categories:
        return categorys_schema.jsonify(categories), 200
    else:
        return jsonify({"message": "Cannot get all category"}), 404

#upadte category by id
def update_category_by_id_service (id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Not found Category"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON data"}), 400
    
    try:
        editable_fields ={"name"}
        for key, value in data.items():
            if key in editable_fields:
                setattr(category, key, value)
        db.session.commit()
        return jsonify({"message": "Update category valid"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Failed to upgrade category", "error": str(e)}),500
    
#delete category by id
def delete_category_by_id_service(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Cannot found category"})
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Delete Category Completed"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Failed delete category", "error": str(e)}), 500