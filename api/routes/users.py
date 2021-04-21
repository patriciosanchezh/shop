from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import  get_jwt_identity
from flask import url_for, render_template_string
from flask_jwt_extended import create_access_token, jwt_required
import datetime

from api.utils.responses import response_with
from api.utils.role_access import access_required, ACCESS
from api.utils import responses as resp
from api.utils.database import db
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.email import send_email
from api.models.users import User, UserSchema 




user_routes = Blueprint("user_routes", __name__)


@user_routes.route('/', methods=['POST'])
@jwt_required()
@access_required('admin') 
def create_user():
    try:
        data = request.get_json()
        if User.find_by_username(data['username']) is not None:
             return response_with(resp.INVALID_INPUT_422)
        data['password'] = User.generate_hash(data['password'])
        user_schmea = UserSchema()
        user = user_schmea.load(data)
        if user.role not in ACCESS.keys(): #check if it's a valid role 
            return jsonify(msg="{} is not a valid role!".format(user.role)), 403
        
        current_user = User.query.get(get_jwt_identity())
        
        if user.role == 'root' and current_user.role != 'root': 
            return jsonify(msg="{You are not allowed to make a root!"), 403
        
        # Comment from this line if you don't want use email.
        
        # token = generate_verification_token(data['email'])  
        # verification_email = url_for('user_routes.verify_email', token=token, _external=True) 
        # html = render_template_string("<p>Welcome! Thanks for signing up. Please follow this link \
        #                               to activate your account:</p> <p><a href='{{ verification_email }}'\
        #                               >{{ verification_email }}</a></p> <br> <p>Thanks!</p>",\
        #                               verification_email=verification_email)
        # subject = "Please Verify your email"
        # send_email(user.email, subject, html)
        
        # Comment to this line if you don't want use email.
        
        user.create()
        return response_with(resp.SUCCESS_201)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/confirm/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except Exception as e:
        print(e)
        return response_with(resp.SERVER_ERROR_401)
    user = User.query.filter_by(email=email).first_or_404()
    if user.isVerified:
        return response_with(resp.INVALID_INPUT_422)
    else:
        user.isVerified = True
        db.session.add(user)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={'message': 'E-mail verified, you can proceed to login now.'})


#In case you don't need verification email, use the next.
# @user_routes.route('/', methods=['POST'])
# @access_required('admin') 
# def create_user():
#     try:
#         data = request.get_json()
#         data['password'] = User.generate_hash(data['password'])
#         user_schmea = UserSchema()
#         user = user_schmea.load(data)
#         if "role" not in data:
#             user.role = 'user'
#         user.create()
#         return response_with(resp.SUCCESS_201)
#     except Exception as e:
#         print(e)
#         return response_with(resp.INVALID_INPUT_422)

@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        if data.get('email'):
            current_user = User.find_by_email(data['email']) 
        elif data.get('username'):
            current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404) 
        
        # Comment from this line if you don't want use email.
        if current_user and not current_user.isVerified: 
            return jsonify(message='User is not verified'), 403   
        #Comment to this line if you don't want use email.
        
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = current_user.id ) #,   expires_delta = False)
            return response_with(resp.SUCCESS_200, \
                                 value={'message': 'Logged in as {}'.format(current_user.username), \
                                        "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

    


#creat a root user as principal administrator
@user_routes.route('/root', methods=['POST'])
def create_root():
    if User.find_by_id(1):
        return jsonify(msg="there is already a root!"), 403
    data = request.get_json()
    data['password'] = User.generate_hash(data['password'])
    user_schmea = UserSchema()
    user = user_schmea.load(data)
    user.role = 'root'
    user.isVerified = True
    user.create()
    return response_with(resp.SUCCESS_201)


#get user list
@user_routes.route('/', methods=['GET'])
@jwt_required()
@access_required('admin') 
def get_user_list():
    get_users = User.query.all()
    user_schema = UserSchema(many=True, only=['id', 'username', 'email', 'role'])
    users = user_schema.dump(get_users)
    return response_with(resp.SUCCESS_200, value={"users": users})

#get complete info of a user
@user_routes.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@access_required('admin') 
def get_user(user_id):
    get_user = User.query.get_or_404(user_id)
    user_schema = UserSchema(only=["id", 'username', 'email', 'role', 'isVerified'])
    user = user_schema.dump(get_user)
    return response_with(resp.SUCCESS_200, value={"user": user})


@user_routes.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@access_required('admin') 
def update_user(user_id):
    try:
        data = request.get_json()
        get_user = User.query.get_or_404(user_id)
        current_user = User.query.get(get_jwt_identity())
        
        if ('root' in data) and current_user.role != 'root': 
            return jsonify(msg="You cannot make a root!"), 403 
        
        for field in data:           #modify only the attributes asked
            setattr(get_user,field, data[field]) 
            
        if "password" in data:      #use the right password
            get_user.password = User.generate_hash(data['password'])
        
        if  get_user.role not in ACCESS.keys():
            return jsonify(msg="{} is not a valid role!".format(get_user.role)), 403
        
        # Comment from this line if you don't want use email.
        # if "email" in data:
        #     get_user.isVerified = False
        #     token = generate_verification_token(data['email'])
        #     verification_email = url_for('user_routes.verify_email', token=token, _external=True)
        #     html = render_template_string("<p>Welcome! Thanks for signing up. Please follow this link \
        #                                   to activate your account:</p> <p><a href='{{ verification_email }}'\
        #                                   >{{ verification_email }}</a></p> <br> <p>Thanks!</p>",\
        #                                   verification_email=verification_email)
        #     subject = "Please Verify your email"
        #     send_email(get_user.email, subject, html)
        # Comment to this line if you don't want use email.
    
        db.session.add(get_user)
        db.session.commit()
        user_schema = UserSchema(only=['id', 'username', 'email', 'role'])
        user = user_schema.dump(get_user)
        return response_with(resp.SUCCESS_200, value={"user": user})
    
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)

@user_routes.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@access_required('admin') 
def delete_user(user_id):
    get_user = User.query.get_or_404(user_id)
    if get_user.username == 'root':
        return jsonify(msg="You can delate a root user!"), 403 
    db.session.delete(get_user)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

@user_routes.route('status/<int:user_id>', methods=['POST'])
@jwt_required()
@access_required('admin') 
def change_status_user(user_id):
    try:
        data = request.get_json()
        get_user = User.query.get_or_404(user_id)
        
        current_user = User.query.get(get_jwt_identity())
    
        if data["role"] not in ACCESS.keys():      #check if it's a valid role 
            return jsonify(msg="{} is not a valid role!".format(data["role"])), 403
        
        if data["role"] == 'root' and current_user.role != 'root': 
            return jsonify(msg="You cannot make a root!"), 403 
        
        get_user.role = data["role"]
        
        db.session.add(get_user)
        db.session.commit()
        return response_with(resp.SUCCESS_200)
    
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)