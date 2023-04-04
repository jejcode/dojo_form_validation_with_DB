#import function to create instance of database
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash # flash allows for validation messages to be sent to html
import re # module for regex
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # global variable to create pattern to validate email
#model the class after the table it represents
class User:
    DB = 'users_schema'
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    #use class methods to call queries
    # CREATE
    @classmethod
    def save(cls,data):
        query = """INSERT INTO users ( first_name,last_name,email )
                VALUES ( %(fname)s, %(lname)s, %(email)s)"""
        return connectToMySQL(cls.DB).query_db(query, data)

    # READ
    @classmethod
    def get_one(cls,user_id): # gets one record from database
        query = """SELECT * FROM users
                WHERE id=%(id)s;"""
        result = connectToMySQL(cls.DB).query_db(query, {'id': user_id}) # don't forget to include query in the query_db!!!
        return cls(result[0]) # create an instance with the result and return it

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users" # query string to send to database
        results = connectToMySQL(cls.DB).query_db(query) # actual query call to database
        users = [] # container for all user objects
        for user in results:
            users.append(cls(user)) # creates an instance of User for each db entry
        return users
    @classmethod
    def check_email(cls, data): # check to see if email exists in db
        query = "SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) == 0:
            return False
        return True
    # UPDATE
    @classmethod
    def update(cls,data): # updates a user record
        query = """UPDATE users
                SET first_name=%(fname)s, last_name=%(lname)s, email=%(email)s
                WHERE id=%(id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data) # don't forget to include query in .query_db!!!
    
    # DELETE
    @classmethod
    def delete(cls,id): # deletes user record according to id
        query = """ DELETE FROM users
                WHERE id=%(id)s"""
        return connectToMySQL(cls.DB).query_db(query, {'id': id}) # don't forget to include query in .query_db!!!
    
    @staticmethod
    def validate_user(user):
        is_valued = True
        
        if  len(user['fname']) <= 0:
            flash("First name is missing.")
            is_valued = False
        if len(user['lname']) <= 0:
            flash('Last name is missing.')
            is_valued = False
        if len(user['email']) <= 0:
            flash('Email is missing.')
            is_valued = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address.')
            is_valued = False
        if User.check_email(user):
            flash('Email already exists. Please enter a different email address.')
            is_valued = False
        return is_valued
    
    # according to the solution, you can loop through the user dictionary and create a message
    # for each case