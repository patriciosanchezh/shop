from api.utils.database import db, ma
from marshmallow import fields


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, 
                   nullable = False)
    
    name = db.Column(db.String(20), \
                     nullable = False)
        
    surname = db.Column(db.String(20), \
                        nullable = False)
    
    email = db.Column(db.String(80), 
                      unique = True, 
                      nullable = False)
            
    photo = db.Column(db.String(500), nullable=True)
    
    created = db.Column(db.DateTime, server_default=db.func.now())
    
    creater_user_id = db.Column(db.Integer, 
                             db.ForeignKey('users.id'), 
                             nullable=False)
    
    last_modifier_user_id = db.Column(db.Integer, 
                                   db.ForeignKey('users.id'), 
                                   nullable=False)
                            
    
    def __init__(self, name, surname, email, creater_user_id, last_modifier_user_id, photo = None):
        self.name = name
        self.surname = surname
        self.photo = photo
        self.email = email
        self.creater_user_id = creater_user_id
        self.last_modifier_user_id  = last_modifier_user_id
        
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


    
class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        include_fk = True # include foreign fields
        load_instance = True
        
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    surname = fields.String(required=True)
    photo = fields.String(required=False)
    email = fields.String(required=True)
    creater_user_id = fields.Number(required=False)
    last_modifier_user_id = fields.Number(required=False)
    