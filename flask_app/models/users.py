
from flask_app.config.mysqlconnection import connectToMySQL
mydb = 'projectsolo'
from flask_app import app
from flask import flash





class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def is_valid(request_form_data):
        is_valid = True
        if len(request_form_data['first_name']) < 1:
            is_valid = False
            flash('First Name Required')
        elif len(request_form_data['first_name']) <= 1:
            is_valid = False
            flash('First Name must be at least 2 characters')
        if len(request_form_data['last_name']) < 1:
            is_valid = False
            flash('Last Name Required')
        elif len(request_form_data['last_name']) < 2:
            is_valid = False
            flash('Last Name must be at least 2 characters')
        return is_valid

    @classmethod
    def get_all(cls):
        query = '''SELECT *
        FROM
        users;'''
        results = connectToMySQL(mydb).query_db(query)
        output = []
        for user_dictionary in results:
            output.append(cls(user_dictionary))
        return output

    @classmethod
    def get_one(cls, data):
        query ="SELECT * FROM users WHERE id = %(id)s"    ;
        result = connectToMySQL(mydb).query_db(query,data)
        return cls(result[0])

    @classmethod
    def register(cls, data):
        query = """INSERT 
        INTO users 
            (first_name, last_name, email, 
            password) 
        VALUES 
            (%(first_name)s, %(last_name)s, %(email)s, 
            %(password)s);
        """
        return connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def update_user(cls, data):
        query = """UPDATE users
        SET 
            first_name = %(first_name)s,
            last_name = %(last_name)s,
            email = %(email)s,
            password = %(password)s
        WHERE 
            id = %(user_py_id)s
        """
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = '''
        SELECT * FROM users WHERE email = %(email)s;
        '''
        result = connectToMySQL(mydb).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


