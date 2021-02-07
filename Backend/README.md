# Server

A Flask-driven RESTful API.

---

## Technologies Used

- [Python](https://www.python.org) - A programming language that lets you work quickly and integrate systems more effectively.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - A Python microframework based on the Pocoo projects, Werkzeug and Jinja2.
- [MySQL](https://www.mysql.com) - A freely available open source Relational Database Management System that uses Structured Query Language (SQL).
- [OMDb API](http://www.omdbapi.com) - A RESTful web service to obtain movies and TV series information.

## Installation / Preparation

- Ensure that you have the latest versions of Python3 and MYSQL globally installed in your computer.

> If you are running macOS, make sure to set Python3 and pip3 as default.

- To install all dependencies go to /Backend/Utils and run the following command:
```
pip install -r requirements.txt
```
- To set the global variables go to /Backend/Utils and create a file configs.py with the following syntax:
```
# OMDb API
OMDB_API_URL = 'http://www.omdbapi.com/'
OMDB_API_KEY = 'your-OMDb-key'

# MySQL Database
DB_USERNAME = 'your-MySQL-username' 
DB_PASSWORD = 'your-MySQL-user-password'
DB_NAME = 'your-MySQL-database-name'

# JWT Authentication
JWT_SECRET_KEY = 'your-JWT-secret-key'
JWT_ALGORITHM = 'JWT-algorithm'
```
> To generate a JWT secret key go to /Backend/Utils and run the following command:
```
sh secretKey.py
```
---

## Usage
