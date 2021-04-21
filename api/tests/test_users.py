import json
from datetime import datetime
import unittest2 as unittest
from flask_jwt_extended import create_access_token
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.test_base import BaseTestCase
from api.models.users import User

def create_users():
    user1 = User(username='ringo', email="ringo@gmail.com", \
                 password=User.generate_hash('hello'), isVerified=True).create()
        
    user2 = User(username='george', email="george@gmail.com", \
                 password=User.generate_hash('hello')).create()
        
    user3 = User(username='john', email= "john@gmail.com", \
                 password=User.generate_hash('hello'), isVerified=True, role ="admin").create()

def login(identity):
    access_token = create_access_token(identity = identity)
    return access_token

class TestUsers(BaseTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        create_users()

    def test_login_user(self):
        
        user = {
          "email" : "ringo@gmail.com",
          "password" : "hello",
        }
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue('access_token' in data)

    def test_login_user_wrong_credentials(self):
        user = {
          "email" : "ringo@gmail.com",
          "password" : "goodbye",
        }
        
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )

        self.assertEqual(401, response.status_code)


    def test_login_unverified_user(self):
        user = {
          "email" : "george@gmail.com",
          "password" : "hello",
        }
        response = self.app.post(
            '/api/users/login',
            data=json.dumps(user),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        
        self.assertEqual(403, response.status_code)
        self.assertTrue('User is not verified' == data['message'])

    def test_create_user_with_authorization(self):
        token = login(3)        #corresponding with user3.id
        
        user = {
            "username": "paul",
           "email" : "paul@gmail.com",
           "password" : "hello",
         }

        response = self.app.post(
             '/api/users/',
             data=json.dumps(user),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
         )

        data = json.loads(response.data)
        
        self.assertEqual(201, response.status_code)
        self.assertTrue('success' in data['code'])
    
    
    def test_create_user_without_authorization(self):
        token = login(1)
        
        user = {
            "username": "paul",
           "email" : "paul@gmail.com",
           "password" : "hello",
         }
        
        response = self.app.post(
             '/api/users/',
             data=json.dumps(user),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
         )
        
        data = json.loads(response.data)
        
        self.assertEqual(403, response.status_code) #not a admin
        self.assertTrue("User needs to be admin", data['msg'])
        
        
    def test_create_user_without_login(self):
        
        user = {
            "username": "paul",
           "email" : "paul@gmail.com",
           "password" : "hello",
         }
        
        response = self.app.post(
             '/api/users/',
             data=json.dumps(user),
             content_type='application/json'
         )

        self.assertEqual(401, response.status_code)
    
    
    def test_create_user_without_username(self):
        token = login(3)
        
        user = {
           "email" : "paul@gmail.com",
           "password" : "hello",
         }

        response = self.app.post(
             '/api/users/',
             data=json.dumps(user),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
         )
        
        self.assertEqual(422, response.status_code)
        
        
    def test_create_user_with_username_exists(self):
        token = login(3)
        
        user = {'username': 'john',
           "email" : "paul@gmail.com",
           "password" : "hello",
         }

        response = self.app.post(
             '/api/users/',
             data=json.dumps(user),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
         )
        
        self.assertEqual(422, response.status_code)
        
    def test_create_user_with_wrong_role(self):
        token = login(3)
        
        user = {'username': 'paul',
           "email" : "paul@gmail.com",
           "password" : "hello",
           "role": "master"
         }

        response = self.app.post(
             '/api/users/',
             data=json.dumps(user),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
         )
        
        data = json.loads(response.data)
        print(data)
        self.assertEqual(403, response.status_code)
        self.assertTrue("master is not a valid role!" == data['msg'])
        

    def test_confirm_email(self):
        token = generate_verification_token('george@gmail.com')

        response = self.app.get(
            '/api/users/confirm/'+token
        )
        data = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertTrue('success' in data['code'])
        
        
    def test_confirm_email_for_verified_user(self):
        token = generate_verification_token('ringo@gmail.com')

        response = self.app.get(
            '/api/users/confirm/'+token)



        self.assertEqual(422, response.status_code)

        
    def test_confirm_email_with_incorrect_email(self):
        token = generate_verification_token('georgeharrison@gmail.com')

        response = self.app.get(
            '/api/users/confirm/' + token)


        self.assertEqual(404, response.status_code)


    def test_get_user(self):
        token = login(3)
        
        user_to_get = User.find_by_email("george@gmail.com")

        response = self.app.get(
              '/api/users/'+str(user_to_get.id),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
          )
        data = json.loads(response.data)
        
        print(data)
        
        user = {'email': 'george@gmail.com', 'id': 2, 'role': 'user', \
                'username': 'george', 'isVerified': False}
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(user == data['user']) #check the user
        
        
    def test_get_user_list(self):
        token = login(3)
        

        response = self.app.get(
              '/api/users/',
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
          )
        data = json.loads(response.data)
        
        list_users = [{'email': 'ringo@gmail.com', 'id': 1, 'role': 'user', 'username': 'ringo'}, \
                      {'email': 'george@gmail.com', 'id': 2, 'role': 'user', 'username': 'george'}, \
                      {'email': 'john@gmail.com', 'id': 3, 'role': 'admin', 'username': 'john'}]
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(list_users == data['users']) #compare list of users

    def test_update_user(self):
        token = login(3)
        
        user = {
            "username": "harrison",
            "email" : "harrison@gmail.com",
            "password" : "something",
            "role": "admin"
          }
        
        response = self.app.put(
              '/api/users/2', #id 2, correponding with george
              data=json.dumps(user),
              content_type='application/json',
              headers= { 'Authorization': 'Bearer '+ token }
          )
        data = json.loads(response.data)
        
        user_updated = {'email': 'harrison@gmail.com', 'id': 2, \
                        'role': 'admin', 'username': 'harrison'}
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(user_updated == data['user']) 
    
    def test_delete_user(self):
        token = login(3)
        
        user = User.find_by_email("george@gmail.com")

        response = self.app.delete(
              '/api/users/'+str(user.id),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
          )

        self.assertEqual(204, response.status_code)
        
    def test_change_status_user(self):
        token = login(3)
        
        data = {"role": "admin"}
        
        user = User.find_by_email("ringo@gmail.com")
        
        response = self.app.post(
              '/api/users/status/'+str(user.id),
              data=json.dumps(data),
            content_type='application/json',
            headers= { 'Authorization': 'Bearer '+ token }
          )
        
        self.assertEqual(200, response.status_code)
        

if __name__ == '__main__':
    unittest.main()