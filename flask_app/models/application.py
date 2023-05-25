
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.dashboard import Dashboard
from flask_app.models.users import Users
mydb = 'projectsolo'





class Application:
    def __init__(self, data):
        self.id = data['id']
        self.building_id = data['building_id']
        self.applicant_id = data['applicant_id']
        self.created_at = data['created_at']
        self.last_address = data['last_address']
        self.birthday = data['birthday']
        self.income = data['income']
        self.moving_date = data['moving_date']
        self.applicant = None
        self.building = None


    @classmethod
    def join_user_to_building(cls, data):
        query = """INSERT 
        INTO applications
            (building_id, applicant_id, last_address, birthday, income, moving_date) 
        VALUES
            (%(building_id)s, %(applicant_id)s, %(last_address)s, %(birthday)s, %(income)s, %(moving_date)s);
        """
        return connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query ='''SELECT * 
        FROM 
            applications 
        WHERE 
            id = %(id)s
        ''';
        result = connectToMySQL(mydb).query_db(query,data)
        return cls(result[0])

    @classmethod
    def has_user_applied(cls, data):
        query = """SELECT 
        COUNT(*) 
        as count 
        FROM applications 
        WHERE 
            building_id = %(building_id)s 
        AND 
            applicant_id = %(applicant_id)s
        """
        result = connectToMySQL(mydb).query_db(query, data)
        return result[0]['count'] > 0

    @classmethod
    def join_application_and_user(cls, data):
        query = '''SELECT *
        FROM applications
        JOIN users 
        ON applications.applicant_id = users.id
        JOIN buildings 
        ON applications.building_id = buildings.id
        WHERE users.id = %(id)s;
        '''
        results = connectToMySQL(mydb).query_db(query, data)
        output = []
        for row in results:
            this_application = cls(row)
            building_data = {
                'id': row['buildings.id'],
                'name': row['name'],
                'address': row['address'],
                'bed': row['bed'],
                'bath': row['bath'],
                'price': row['price'],
                'created_at': row['buildings.created_at'],
                'updated_at': row['updated_at'],
                'description': row['description'],
                'seconddescription': row['seconddescription']
            }
            this_application.building = Dashboard(building_data)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['updated_at']
            }
            this_application.applicant = Users(user_data)
            output.append(this_application)
        return output

    @classmethod
    def deleteApplication(cls, data):
        query = "DELETE FROM applications WHERE id = %(id)s";
        return connectToMySQL(mydb).query_db(query, data)

    
    @classmethod
    def join_user_to_building_update(cls, data):
        query = """UPDATE applications
        SET 
            building_id = %(building_id)s,
            applicant_id = %(applicant_id)s,
            last_address = %(last_address)s,
            birthday = %(birthday)s,
            income = %(income)s,
            moving_date = %(moving_date)s
        WHERE 
            id = %(id)s
        """
        results = connectToMySQL(mydb).query_db(query, data)
        print(results)
        return results


