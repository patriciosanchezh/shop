from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.customers import Customer, CustomerSchema
from api.models.users import User
from api.utils.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, url_for, current_app
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

customer_routes = Blueprint("customer_routes", __name__)


@customer_routes.route('/', methods=['POST'])
@jwt_required() 
def create_customer():
    try:
        data = request.get_json()
        customer_schema = CustomerSchema()
        data["creator_user_id"] = get_jwt_identity()
        data["last_modifier_user_id"] = get_jwt_identity()
        customer = customer_schema.load(data)
        result = customer_schema.dump(customer.create())
        return response_with(resp.SUCCESS_201, value={"customer": result})

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@customer_routes.route('/photo/<int:customer_id>', methods=['POST'])
@jwt_required()
def upsert_customer_avatar(customer_id):
    try:
        file = request.files['photo']
        get_customer = Customer.query.get_or_404(customer_id)         
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            filename = str(get_customer.id) + "." + extension       #save photo with customer.id plus original extension
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
            if get_customer.photo:           #remove old photo if it exists
                old_photo = get_customer.photo.split("/")[-1]
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], old_photo))
                
        get_customer.photo = url_for('uploaded_file', filename = filename, _external=True)
        get_customer.last_modifier_user = get_jwt_identity()
        db.session.add(get_customer)
        db.session.commit()
        customer_schema = CustomerSchema()
        customer = customer_schema.dump(get_customer)
        return response_with(resp.SUCCESS_200, value={"customer": customer})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@customer_routes.route('/', methods=['GET'])
@jwt_required()
def get_customer_list():
    get_customers = Customer.query.all()
    customer_schema = CustomerSchema(many=True,  only=['id','name', 'surname', 'email',\
                                                       'last_modifier_user_id',\
                                                       'creator_user_id'])
    customers = customer_schema.dump(get_customers)
    return response_with(resp.SUCCESS_200, value={"customers": customers})

@customer_routes.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    get_customer = Customer.query.get_or_404(customer_id)
    customer_schema = CustomerSchema()
    customer = customer_schema.dump(get_customer)
    return response_with(resp.SUCCESS_200, value={"customer": customer})
    

@customer_routes.route('/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    try:
        data = request.get_json()
        get_customer = Customer.query.get_or_404(customer_id)
        for field in data:
            setattr(get_customer,field, data[field]) 

        get_customer.last_modifier_user_id = get_jwt_identity()
        db.session.add(get_customer)
        db.session.commit()
        customer_schema = CustomerSchema(only=['id','name', 'surname', 'email',\
                                                       'last_modifier_user_id',\
                                                       'creator_user_id'])
        customer = customer_schema.dump(get_customer)
        return response_with(resp.SUCCESS_200, value={"customer": customer})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@customer_routes.route('/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    get_customer = Customer.query.get_or_404(customer_id)
    db.session.delete(get_customer)
    db.session.commit()
    return response_with(resp.SUCCESS_204)
