# Project Title

This project consists in a REST API for managing customer data for a small shop. There are 2 groups with different endpoints: users and customers. The users can have only 3 different roles (root, admin and user), and depending of that, they are allowed to make more things. The root is the first user and he has to be created first in order to create more users or admins. The tasks are the following:

user can:• List all customers in the database.• Get full customer information, including a photo URL.• Create a new customer:	• All customer have name, surname, id, email (unique), creator user, 
	last modifier user, date created and URL photo.
	• name, surname and email are required.• Upload a photo for each user. • Update an existing customer.• Delete an existing customer.

Any of the last functions require user to be logged.

An admin can also:• Create users. Users have the fields id, username (unique), email (unique), password,
 		role and isVerified. All of them are required but role and isVerified,
		which are user and False, by default and respectably. In order to valid
		the authentication, a email is sent to verify the identity. • Delete users.• Update users.• List users.• Change admin status. 




Main libraries used:
1. Flask - API design and working with third party APIs
2. Flask-SQLAlchemy - adds support for SQLAlchemy ORM.


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
        $ python3 -m venv venv
	$ source ./venv/bin/activate 
    ```

* #### Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
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
│   │	│   └── db.slite
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




## Run app ##

* Before Running enter to src.
	
    ```
         (venv) flask-rest-api $ cd src
    ```

* It must looks like this

    ```
   	 (venv) flask-rest-api/src $
    ```

* Now before run, we have to make a changes in src/api/conifg/conifg.py in the class DevelopmentConfig. In order to send the email for Auth 2 protocol for authentication, use your own credentials for these fields:

    ```
    MAIL_DEFAULT_SENDER= '<mail_sender>'
    MAIL_SERVER= '<mail_smtp_host>'
    MAIL_PORT= '<mail_port>'
    MAIL_USERNAME= '<mail_username>'
    MAIL_PASSWORD= '<mail_password>'
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True 
    ```
*All this info you can find in your email, configurations. Some servers require a previous configuration in its site. By example, I used a scholar email server. 

* Now you are ready to run it.

    On your terminal, run the server using this one simple command:

    ```
    (venv) flask-rest-api/src $ pyhon run.py
    ```

    You can now access the app on your local browser by using

    ```
    http://localhost:5000/api/
    ```


```
Give the example
```

## Run app ##

  `$ python ./run.py`

The app will be running in `localhost:5000`

And repeat

## Usage
### Users endpoint

First you need to create the first user, which will have the role of root. This endpoint is only possible for 1 time. 

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


POST http://127.0.0.1:5000/api/users/login


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

For the rest endpoints in users you need to login in and the user's role has to be at least admin. There is an order in roles, user = 1, admin = 2, and root = 3. This can be modify and add more users with different authorizations. 




## Running the tests

*In order the test for users
    ```
    (venv) flask-rest-api/src $ nosetests api/tests/test_users.py
    ```

It will be run 17 tests, with different configurations, simulating all the functions, with authorization or not. See src/api/test/test_users.py to see them. Exactly they do:



*For the test for customers

In order the test for users
    ```
    (venv) flask-rest-api/src $ nosetests api/tests/test_customers.py
    ```

It will be run 9 tests.




## Authors

* **Patricio Sánchez** - 



