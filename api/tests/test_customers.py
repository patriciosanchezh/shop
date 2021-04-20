import json
from api.utils.test_base import BaseTestCase
from api.models.customers import Customer
from api.models.users import User
from datetime import datetime
from flask_jwt_extended import create_access_token
import unittest2 as unittest
import io


def create_users():
    user1 = User(username='ringo', email="ringo@gmail.com", \
                 password=User.generate_hash('hello'), isVerified=True).create()
    user2 = User(username='john', email= "john@gmail.com", \
                 password=User.generate_hash('hello'), isVerified=True, role ="admin").create()

def create_customers():
    customer1 = Customer(name="Elthon", surname="John", email = "elthon@gmail.com",\
                         creator_user_id=1, last_modifier_user_id=1).create()
    customer2 = Customer(name="Mick", surname="Jagger", email = "mick@gmail.com",\
                         creator_user_id=1, last_modifier_user_id=1).create()



def login(identity):
    access_token = create_access_token(identity = identity )
    return access_token


class TestCustomers(BaseTestCase):
    def setUp(self):
        super(TestCustomers, self).setUp()
        create_customers()
        create_users()

    def test_create_customer(self):
        token = login(1)    #corresponding with user1.id
        customer = {
            'name': 'Roger',
            'surname': 'Waters',
            'email': 'waters@gmail.com'
        }

        response = self.app.post(
            '/api/customers/',
            data=json.dumps(customer),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer ' + token }
        )
        
        
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('customer' in data)
        
    def test_create_customer_no_authorization(self):
        customer = {
            'name': 'Roger',
            'surname': 'Waters',
            'email': 'waters@gmail.com'
        }

        response = self.app.post(
            '/api/customers/',
            data=json.dumps(customer),
            content_type='application/json',
        )

        self.assertEqual(401, response.status_code)

    def test_create_customer_no_email(self):
        token = login(1)    #corresponding with user1.id
        customer = {
            'name': 'Roger',
            'surname': 'Waters'
        }

        response = self.app.post(
            '/api/customers/',
            data=json.dumps(customer),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+token }
        )
        
        self.assertEqual(422, response.status_code)

    def test_upload_photo(self):
        token = login(1)     #corresponding with user1.id
        
        response = self.app.post(
            '/api/customers/photo/2',
            data=dict(photo=(io.BytesIO(b'test'), 'test_file.jpg')),
            content_type='multipart/form-data',
            headers= { 'Authorization': 'Bearer '+ token }
        )
        self.assertEqual(200, response.status_code)
    
    
    def test_upload_photo_without_file(self):
        token = login(1)
        
        response = self.app.post(
            '/api/customers/photo/2',
            data=dict(file=(io.BytesIO(b'test'), 'test_file.csv')),
            content_type='multipart/form-data',
            headers= { 'Authorization': 'Bearer '+ token }
        )
        self.assertEqual(422, response.status_code)


    def test_get_customers(self):
        token = login(1)
        
        response = self.app.get(
            '/api/customers/',
            content_type='application/json',
                        headers= { 'Authorization': 'Bearer '+ token }
        )
        data = json.loads(response.data)
        
        customers = [{'creator_user_id': 1.0, 'email': 'elthon@gmail.com', 'id': 1.0, \
                       'last_modifier_user_id': 1.0, 'name': 'Elthon', 'surname': 'John'},\
                      {'creator_user_id': 1.0, 'email': 'mick@gmail.com', 'id': 2.0, \
                       'last_modifier_user_id': 1.0, 'name': 'Mick', 'surname': 'Jagger'}]
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(customers == data['customers'])


    def test_get_customer_detail(self):
        token = login(1)
        
        response = self.app.get(
            '/api/customers/2',
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
            )
        
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        
        self.assertTrue('customer' in data)


    def test_update_customer_and_change_last_modifier(self):
        token = login(2)   
        customer = {
            'name': 'Michael'
        }
        response = self.app.put(
            '/api/customers/2',
            data=json.dumps(customer),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+token }
        )
        data = json.loads(response.data)

        
        customer_modified  = {'creator_user_id': 1.0, 'email': 'mick@gmail.com', 'id': 2.0, \
                       'last_modifier_user_id': 2.0, 'name': 'Michael', 'surname': 'Jagger'}
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(customer_modified == data['customer'])
    
    
    def test_delete_customer(self):
        token = login(1)
        
        response = self.app.delete(
            '/api/customers/2',
            headers= { 'Authorization': 'Bearer '+token }
        )
        self.assertEqual(204, response.status_code)





if __name__ == '__main__':
    unittest.main()