# Project Title

This project consists in a REST API for managing customer data for a small shop. There are 2 groups with different endpoints: users and customers. The users can have only 3 different roles (root, admin and user), and depending of that, they are allowed to make more things. The root is the first user and he has to be created first in order to create more users or admins. The tasks are the following:

A user can:• List all customers in the database.• Get full customer information, including a photo URL.• Create a new customer:	• All customers have name, surname, id, email (unique), creator user, 
	last modifier user, date created and URL photo.
	• name, surname and email are required.• Upload a photo for each user. • Update an existing customer.• Delete an existing customer.

Any of the last functions require the user to be logged in.

An admin can also:• Create users. Users have the fields id, username (unique), email (unique), password,
 		role and isVerified (which indicates if the user has a confirmation via 		email). All of them are required. By default, role = user and isVerified = 		False. In order to valid the authentication, an email is sent to verify 		the identity. • Delete users.• Update users.• List all users.• Change admin status. 





## Prerequisites

python 3.8.6

Flask==1.1.2

Flask-JWT-Extended==4.1.0

Flask-Login==0.5.0

Flask-Mail==0.9.1

flask-marshmallow==0.14.0

Flask-SQLAlchemy==2.5.1

marshmallow-sqlalchemy==0.24.2

nose==1.3.7

passlib==1.7.4

unittest2==1.1.0


## Installation 

This project was made in macOS catalina, the commands for another OS can be different.

* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).

* Now, type the following command to create a new directory of name flask-rest-api and open it in your terminal.
    ```
        $ mkdir flask-rest-api && cd flask-rest-api
    ```


* Git clone this repo to your computer
    ```
        flask-rest-api $ git clone https://github.com/patriciosanchezh/shop.git
    ```


* Rename the directory shop to src. This is necessary in oder to run the test using library nose, if you know a better way, please let me know.

    ```
        $ mv shop src
    ```

* Create and activate your virtual environment in python3:
    ```
        flask-rest-api $ python3 -m venv venv
	flask-rest-api $ source ./venv/bin/activate 
	(venv)$
    ```

* #### Install your requirements
    ```
	(venv) flask-rest-api $ pip install -r src/requirements.txt
    ```



## Project structure:

Now the project must look like this.
```
venv/
src
├── README.md
├── run.py
├── main.py
├── __init__.python
├── api
│   ├── __init__.python
│   ├── config
│   │   ├── __init__.py
│   │	├── database
│   │	│   └── db.sqlite
│   │   └── config.py
│   ├── models  
│   │   ├── __init__.py
│   │   ├── customers.py
│   │   └── users.py
│   ├── routes
│   │   ├──  __init__.py
│   │   ├── customers.py
│   │   └── users.py
│   ├── test
│   │   ├──  __init__.py
│   │   ├── test_customers.py
│   │   └── test_users.py
│   ├── utils
│   │   ├──  __init__.py
│   │   ├── database.py
│   │   ├── email.py
│   │   ├── responses.py
│   │   ├── role_access.py
│   │   ├── test_base.py
│   │   └── token.py
├── images
└── requirements.txt

```


The endpoints are defined in routes. The models which defined users and customers for the database are in models. 


## Run app ##

* Before Running enter to src.
	
    ```
         (venv) flask-rest-api $ cd src
    ```

* It must looks like this

    ```
   	 (venv) flask-rest-api/src $
    ```

* Now before running, you have to make some changes in src/api/conifg/conifg.py in the class DevelopmentConfig. In order to send the email for Auth 2 protocol for authentication, use your own credentials for these fields:

    ```
    MAIL_DEFAULT_SENDER= '<mail_sender>'
    MAIL_SERVER= '<mail_smtp_host>'
    MAIL_PORT= '<mail_port>'
    MAIL_USERNAME= '<mail_username>'
    MAIL_PASSWORD= '<mail_password>'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True 
    ```
* You can find all this info in your email configurations. Some servers require a previous configuration in its site. For example, I used a scholar email server. 

* NOTE: If you do not want to deal with emails, you can comment several lines in the functions authenticate_user, create_user and update_user in api/routes/users.py. The exact lines are indicated.

* NOTE: Email credentials are not required for the test.

* The database with users and customers will be in api/config/database/db.sqlite. If you want a clean database type:


    ```
	(venv) flask-rest-api/src $ rm api/config/database/db.sqlite
    ```

Each time you use the app you get the last database. It's possible to connect to a sql server too.

* Now you are ready to run it.

    On your terminal, run the server using this one simple command:

    ```
    (venv) flask-rest-api/src $ pyhon run.py
    ```

    You can now access the app on your local browser by using:

    ```
    http://localhost:5000/api/
    ```




## Usage

### Users endpoint

First you need to create the first user, which will have the role of root. This endpoint is only possible for 1 time. 

* Create root

POST http://127.0.0.1:5000/api/users/root

REQUEST
```json
{
	"username": "ringo",
	"email": "ringo@gmail.com",
	"password": "hello"
}
```


RESPONSE
```json
{
"code": "success",
}
```

This user doesn't need to be verified. 

* Login user

POST http://127.0.0.1:5000/api/users/login


REQUEST
```json
{
	"username": "ringo",
	"email": "ringo@gmail.com",
	"password": "hello"
}
```

You can use username or email; the password is required. The user needs to be verified.

RESPONSE
```json
{

    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODk5OTQ5NCwianRpIjoiMmNhYWIxMTgtYTlkZS00MDYwLTliYzUtNzgwNzBjODYwMmI2IiwibmJmIjoxNjE4OTk5NDk0LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkwMDAzOTR9.7FkiWB0cfpHdOOmI9U32Dnc5m-ox_ORB_hA7mAeWK-U",
    "code": "success",
    "message": "Logged in as ringo"

}

```

This access_token will be used to log in. 


*VERY IMPORTANT NOTE: For the rest endpoints in customers you need to log in and for the endpoints in users, you also need the user's role to be at least admin. There is an order in roles, user = 1, admin = 2, and root = 3. This can be modified and add more users with different authorizations. 


* Create user

POST http://127.0.0.1:5000/api/users/

REQUEST

```json{
Header {Authorization: 

Barear eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODk5OTQ5NCwianRpIjoiMmNhYWIxMTgtYTlkZS00MDYwLTliYzUtNzgwNzBjODYwMmI2IiwibmJmIjoxNjE4OTk5NDk0LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJleHAiOjE2MTkwMDAzOTR9.7FkiWB0cfpHdOOmI9U32Dnc5m-ox_ORB_hA7mAeWK-U}



}
```



```json{

{
	"username": "paul",
	"email" : "paul@gmail.com",
	"password" : "hello"
}


}

```
You can add the role. You can put root only if you are logged in as a user with role root.


NOTE: We omit writing the header in the following but it's necessary. 

If it's a valid email you will get:

RESPONSE
```json
{

    "code": "success"
}

```

Open the link in the email and see:

RESPONSE
```json
{"code":"success","message":"E-mail verified, you can proceed to login now."}

```

*IMPORTANT NOTE: If you do not want to deal with emails, you can comment several lines in the functions authenticate_user, create_user and update_user in api/routes/users.py. The exact lines are indicated.



If the token has expired:


RESPONSE
```json
{
    "msg": "Token has expired"
}
```
* NOTE: You can change the time, in confirm_verification_token(token, expiration=1800), in api/utils/token.py. Also you can put tokens with no expiration in the parameters of  create_access_token(... expires_delta= False). This in the function authenticate_user, in api/routes/users.py.


* Get user list


GET http://127.0.0.1:5000/api/users/

REPONSE

```json
{
    "code": "success",
    "users": [
        {
            "email": "ringo@gmail.com",
            "id": 1,
            "role": "root",
            "username": "ringo"
        },
        {
            "email": "paul@gmail.com",
            "id": 2,
            "role": "user",
            "username": "paul"
        }
    ]
}
```

* Get user 

GET http://127.0.0.1:5000/api/users/1

REPONSE

```json
{
    "code": "success",
    "user": {
        "email": "ringo@gmail.com",
        "id": 1,
        "isVerified": true,
        "role": "root",
        "username": "ringo"
    }
}
```

* Update user

PUT http://127.0.0.1:5000/api/users/2

```json
{
        "username": "maccartney",
        "password" : "yesterday"
}

```



RESPONSE

```json
{
    "code": "success",
    "user": {
        "email": "paul@gmail.com",
        "id": 2,
        "role": "user",
        "username": "maccartney"
    }
}

```

* Change status user

PUT http://127.0.0.1:5000/api/users/status/2

```json
{
"role": "admin"
}

```

RESPONSE

```json
{
    "code": "success"
}

```


* Delete user

DELETE http://127.0.0.1:5000/api/users/2

404 NO CONTENT


### Customers endpoint


NOTE: We omit the header with the authorization in the following but it's necessary. 

* Create customer


POST http://127.0.0.1:5000/api/customers/

REQUEST


```json{

{
    "name": "Roger",
    "surname": "Waters",
    "email": "waters@gmail.com"

}


}

```


RESPONSE
```json
{
    "code": "success",
    "customer": {
        "creator_user_id": 1.0,
        "email": "waters@gmail.com",
        "id": 1.0,
        "last_modifier_user_id": 1.0,
        "name": "Roger",
        "photo": null,
        "surname": "Waters"
    }
}

```

* Upload photo

POST http://127.0.0.1:5000/api/customers/photo/1

REQUEST
*Use content_type='multipart/form-data' and export the choose file: waters.jpg


RESPONSE
```json
{
    "code": "success",
    "customer": {
        "creator_user_id": 1.0,
        "email": "waters@gmail.com",
        "id": 1.0,
        "last_modifier_user_id": 1.0,
        "name": "Roger",
        "photo": "http://127.0.0.1:5000/photo/1.jpg",
        "surname": "Waters"
    }
}




```


Each time you upload a new photo, the old one is deleted. The number after photo/ corresponds to customer.id.


* Get user list


GET http://127.0.0.1:5000/api/customers/

REPONSE

```json
{
    "code": "success",
    "customers": [
        {
            "creator_user_id": 1.0,
            "email": "waters@gmail.com",
            "id": 1.0,
            "last_modifier_user_id": 1.0,
            "name": "Roger",
            "surname": "Waters"
        },
        {
            "creator_user_id": 1.0,
            "email": "elthon@gmail.com",
            "id": 2.0,
            "last_modifier_user_id": 1.0,
            "name": "Elthon",
            "surname": "John"
        }
    ]
}
```

* We added Elthon John before.

* Get user 

GET http://127.0.0.1:5000/api/customers/1

REPONSE

```json
{
    "code": "success",
    "customer": {
        "creator_user_id": 1.0,
        "email": "waters@gmail.com",
        "id": 1.0,
        "last_modifier_user_id": 1.0,
        "name": "Roger",
        "photo": "http://127.0.0.1:5000/photo/1.jpg",
        "surname": "Waters"
    }
}
```

* Update customer

PUT http://127.0.0.1:5000/api/users/2

```json
{
    "name": "Rogelio",
    "surname": "Aguas",
    "email": "rogelio@gmail.com"

}

```



RESPONSE

```json
{
    "code": "success",
    "customer": {
        "creator_user_id": 1.0,
        "email": "rogelio@gmail.com",
        "id": 1.0,
        "last_modifier_user_id": 1.0,
        "name": "Rogelio",
        "surname": "Aguas"
    }
}

```




* Delete customer

DELETE http://127.0.0.1:5000/api/customers/1

404 NO CONTENT





## Run the tests ##



* Recall to rename the directory shop to src.

* In order to run the tests for users:

```
    (venv) flask-rest-api/src $ nosetests api/tests/test_users.py
```

It will run 17 tests, with different configurations, simulating all the functions, with authorization or not. See src/api/test/test_users.py to get more details. 






In order to run the test for customers:
   
```
    (venv) flask-rest-api/src $ nosetests api/tests/test_customers.py
```

It will  run 9 tests, with different configurations, simulating all the functions, with authorization or not. See src/api/test/test_customers.py to get more details. 




## Author

* **Patricio Sánchez** 



