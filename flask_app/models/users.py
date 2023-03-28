from ..config.mysqlconnection import connectToMySQL
from flask import flash
# from ..models import recipes
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-z]+')
class Users:
    db = 'foodie'
    def __init__(self, data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_deleted = data['is_deleted']
        self.user_orders = []

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users WHERE is_deleted = 0;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])
        

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (user_name, email, password) VALUE (%(user_name)s, %(email)s, %(password)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash(u'Invalid email address!', 'register')
            is_valid = False
        if len(user['user_name']) < 2:
            flash(u'Invalid user name!', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash(u'Password must be at least 8 characters', 'register')
            is_valid = False
        return is_valid