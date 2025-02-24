from flask import request, Blueprint
from .services import (add_category_service, get_category_by_id_service,
                       update_category_by_id_service, get_all_category_service,
                       delete_category_by_id_service)

categorys = Blueprint('categorys', __name__) 

#add category
@categorys.route("/managementBook/addCategory", methods=['POST'])
def add_category():
    return add_category_service()   

#get category by id
@categorys.route("/managementBook/Category/<int:id>", methods=['GET'])
def get_category_by_id(id):
    return get_category_by_id_service(id)

#get all category
@categorys.route("/managementBook/allCategory", methods=['GET'])
def get_all_category():
    return get_all_category_service()

#update category by id
@categorys.route("/managementBook/Category/<int:id>", methods=["PUT"])
def update_category_by_id(id):
    return update_category_by_id_service(id)

#delete category by id
@categorys.route("/managementBook/Category/<int:id>", methods=["DELETE"])
def delete_category_by_id(id):
    return delete_category_by_id_service(id)
