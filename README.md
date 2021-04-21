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

## Project structure:
```
.
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
## Installation / Usage
* If you wish to run your own build, first ensure you have python3 globally installed in your computer. If not, you can get python3 [here](https://www.python.org).
* After this, ensure you have installed virtualenv globally as well. If not, run this:
    ```
        $ pip install virtualenv
    ```
* Git clone this repo to your PC
    ```
        $ git clone git@github.com:gitgik/flask-rest-api.git
    ```


* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```
        $ cd flask-rest-api
        ```

    2. Create and fire up your virtual environment in python3:
        ```
        $ virtualenv -p python3 venv
        $ pip install autoenv
        ```

* #### Environment Variables
    Create a .env file and add the following:
    ```
    source venv/bin/activate
    export SECRET="some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
    export APP_SETTINGS="development"
    export DATABASE_URL="postgresql://localhost/flask_api"
    ```

    Save the file. CD out of the directory and back in. `Autoenv` will automagically set the variables.
    We've now kept sensitive info from the outside world! 😄

* #### Install your requirements
    ```
    (venv)$ pip install -r requirements.txt
    ```

* #### Migrations
    On your psql console, create your database:
    ```
    > CREATE DATABASE flask_api;
    ```
    Then, make and apply your Migrations
    ```
    (venv)$ python manage.py db init

    (venv)$ python manage.py db migrate
    ```

    And finally, migrate your migrations to persist on the DB
    ```
    (venv)$ python manage.py db upgrade
    ```

* #### Running It
    On your terminal, run the server using this one simple command:
    ```
    (venv)$ flask run
    ```
    You can now access the app on your local browser by using
    ```
    http://localhost:5000/bucketlists/
    ```
    Or test creating bucketlists using Postman

## Getting Started

First create a directory

Now clone the directory.

gh repo clone patriciosanchezh/shop

python3.8 -m venv shop 

python 3.8

In the mail directory there


Each time a new photo is uploaded, the old one is deleted in the database.

Any of the last functions require  to be logged.

mkdir author-manager && cd author-manager

source ./shop/bin/activate 

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

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


```
Give examples
```

### Installing

pip install -r requirements.txt

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

## Run app ##

  `$ python ./run.py`

The app will be running in `localhost:5000`

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

In order to run the tests the main folder must have the name src. 




### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Patricio Sánchez** - 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

