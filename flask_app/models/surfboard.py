from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Surfboard:
    def __init__( self , data ):
        self.id = data['id']
        self.board_name = data['board_name']
        self.user_id = data["user_id"]
        self.year = data['year']
        self.shaper = data['shaper']
        self.volume = data['volume']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    
    
    @classmethod
    def save(cls, data):
        #always have to pass in"cls" because it's a class method
        query = """
                INSERT INTO surfboards (user_id, board_name, year, shaper, volume, created_at, updated_at) 
                VALUES (%(user_id)s,%(board_name)s, %(year)s, %(shaper)s, %(volume)s,  NOW(), NOW());
             """
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('surfboards').query_db(query, data)
    
    @classmethod
    def get_by_user_id(cls, user_id):
        print("user_id:", user_id)
        query = "SELECT * FROM surfboards WHERE user_id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL('surfboards').query_db(query, data)
        surfboards = []
        for result in results:
            surfboards.append(cls(result))
        return surfboards
    
    @classmethod
    def get_all_surfboards_with_users(cls):
        query = "SELECT surfboards.*, users.first_name FROM surfboards JOIN users ON surfboards.user_id = users.id;"
        results = connectToMySQL('surfboards').query_db(query)
        surfboards_with_users = []
        for row in results:
            surfboards_with_users.append(cls(row))
        return surfboards_with_users
    
    @classmethod
    def delete_surfboards(cls, id):
        query = "DELETE FROM surfboards where id = %(id)s"
        
        return connectToMySQL('surfboards').query_db(query, {"id": id})
    
    @classmethod
    def get_surfboard_by_id(cls, surfboard_id):
        query = "SELECT surfboards.*, users.first_name FROM surfboards JOIN users ON surfboards.user_id = users.id WHERE surfboards.id = %(id)s"
        result = connectToMySQL('surfboards').query_db(query, surfboard_id)
        if result:
            return cls(result[0])
        return None
    #I fixed an error above. I was passing a dictionary instead of passing the surfboard_id parameter directly.
    @classmethod
    def update(cls, data):
        query = """
            UPDATE surfboards
            SET board_name = %(board_name)s, volume = %(volume)s, shaper = %(shaper)s, year = %(year)s, updated_at = NOW()
            WHERE id = %(id)s;
            """
        return connectToMySQL('surfboards').query_db(query, data)

    @staticmethod
    def validate_surfboard(surfboard):
        is_valid = True
        if len(surfboard['board_name']) < 3:
            flash("Must enter surfboard name")
            is_valid = False
        if len(surfboard['volume']) < 1:
            flash("Must enter volume")
            is_valid = False
        if len(surfboard['shaper']) < 3:
            flash("Must enter instructions")
            is_valid = False
        if len(surfboard['year']) < 4:
            flash("Must enter four digit year")
            is_valid = False
        return is_valid
    
   