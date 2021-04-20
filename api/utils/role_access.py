from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from api.models.users import User


ACCESS = {
    'user': 1,
    'admin': 2,
    'root': 3
}


#decorator that verifies the JWT role
def access_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user = User.find_by_email(get_jwt_identity())
            if ACCESS[current_user.role] >= ACCESS[role]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="User needs to be {}!".format(role)), 403

        return decorator

    return wrapper