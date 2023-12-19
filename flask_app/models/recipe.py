from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    DB = "recipes_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_cooked = data['date_cooked']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.creator = None
    
    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO recipes (name, description, instructions, under_30, date_cooked, user_id)
                VALUES (%(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_cooked)s, %(user_id)s);
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def update(cls, data):
        query = """
                UPDATE recipes
                SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(inder_30)s, date_cooked = %(date_cooked)s, updated_at = NOW()
                WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    @classmethod
    def get_by_id(cls, id):
        query = """
                SELECT * FROM recipes
                JOIN users ON users.id = recipes.user_id
                WHERE recipes.id = %(id)s;
        """
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            row = results[0]
            creator_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            recipe = cls(row)
            recipe.creator = user.User(creator_data)
            return recipe
        else:
            return False
    
    @classmethod
    def get_with_user(cls):
        query = """
                SELECT * FROM recipes
                LEFT JOIN users ON users.id = recipes.user_id;
        """
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            recipes = []
            for row in results:
                creator_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                recipe = cls(row)
                recipe.creator = user.User(creator_data)
                recipes.append(recipe)
            return recipes
        else:
            return False
        
    @staticmethod
    def validate_new_recipe(recipe):
        is_valid = True
        if (recipe.get('name') == ""):
            flash('Name cannot be blank')
            is_valid = False
        if (recipe.get('description') == ""):
            flash('Description cannot be blank')
            is_valid = False
        if (recipe.get('instructions') == ""):
            flash('Instructions cannot be blank')
            is_valid = False
        if (recipe.get('under_30') == None):
            flash('Please mark if recipe is greater than or less than 30 minutes')
            is_valid = False
        if (recipe.get('date_cooked') == ""):
            flash('Please add a date for when this recipe was made')
            is_valid = False
        return is_valid