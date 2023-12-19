from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "recipes_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_by_id(cls, id):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s
        """
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        print(results)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_new_user(user):
        is_valid = True
        if (user.get('password') == None) or (len(user['first_name']) < 2):
            flash('Invalid first name! Please use 2 or more characters', 'register')
            is_valid = False
        if (user.get('password') == None) or (len(user['last_name']) < 2):
            flash('Invalid last name! Please use 2 or more characters', 'register')
            is_valid = False
        if (user.get('email') == None) or (not EMAIL_REGEX.match(user['email'])):
            flash('Invalid email! Please try again', 'register')
            is_valid = False
        elif User.get_by_email(user):
            flash('This email already exists. Please enter another', 'register')
            is_valid = False
        if (user.get('password') == None) or (len(user['password']) < 8):
            flash('Invalid Password! Please use 8 or more characters!', 'register')
            is_valid = False
        elif user['password-confirm'] != user['password']:
            flash('Passwords do not match! Please Try Again', 'register')
            is_valid = False
        return is_valid
