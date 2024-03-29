from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

db ='mamas_night2'
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
                """
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = """INSERT INTO users ( first_name , last_name , username, email, password )
                VALUES (  %(first_name)s , %(last_name)s , %(username)s, %(email)s, %(pw_hash)s );"""
        return connectToMySQL(db).query_db(query,data)



    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_reg(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        if len(data['email']) <= 0:
            flash("Email is required", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email!", "register")
            is_valid = False
        query = """
                SELECT * FROM users WHERE email = %(email)s;
                """
        results = connectToMySQL(db).query_db(query, data)
        if len(results) != 0:
            flash("Email already being used", "register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid
        if data['password'] != data ['confirm_password']:
            flash("Password does not match")
            is_valid = False
        return is_valid
