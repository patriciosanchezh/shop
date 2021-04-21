from passlib.hash import pbkdf2_sha256 as sha256
from marshmallow import fields
from api.utils.database import db, ma



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String(30),
                         unique = True, 
                         nullable = False)
        
    email = db.Column(db.String(50), 
                      unique = True, 
                      nullable = False)
    
    isVerified = db.Column(db.Boolean,  
                           nullable=False, 
                           default=False)
    
    password = db.Column(db.String(120), 
                         nullable = False)
    
    role = db.Column(db.String(120), 
                         nullable = False)
    
    def __init__(self, username, email, password, role = "user", isVerified = False):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.isVerified = isVerified
        
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
    
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
    



#Schema for User
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=False)
    isVerified = fields.Boolean(dump_only=True)