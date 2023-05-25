
from flask_app.config.mysqlconnection import connectToMySQL
mydb = 'projectsolo'





class Dashboard:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.address = data['address']
        self.bed = data['bed']
        self.bath = data['bath']
        self.price = data['price']
        self.description = data['description']
        self.seconddescription = data['seconddescription']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls):
        query = '''SELECT *
        FROM
        buildings;'''
        results = connectToMySQL(mydb).query_db(query)
        output = []
        for user_dictionary in results:
            # new_user = cls(user_dictionary)
            # output.append(new_user)
            # print(user_dictionary)
            output.append(cls(user_dictionary))
        return output

    @classmethod
    def get_one(cls, data):
        query = '''SELECT *
        FROM buildings
        WHERE id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query, data)
        return cls(results[0])


