from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

db ='mamas_night2'
class Movie:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.picked_by = data['picked_by']
        self.date_watched = data['date_watched']
        self.description = data['description']
        self.fav_quote = data['fav_quote']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM movies;"
        results = connectToMySQL(db).query_db(query)
        movies = []
        for movie in results:
            movies.append(cls(movie))
        return movies

    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO movies( title, picked_by, date_watched, description, fav_quote, comments, user_id)
                VALUES ( %(title)s, %(picked_by)s, %(date_watched)s, %(description)s, %(fav_quote)s,
                        %(comments)s, %(user_id)s);
                """
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_one(cls,id):
        query = """
                SELECT * FROM movies WHERE id = %(id)s;
                """
        data = {'id': id}
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def comment(cls,data):
        query = """
                INSERT INTO comments (movie_id, user_id)
                VALUES (%(movie_id)s, %(user_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def update(cls,data):
        query = """
                UPDATE movies SET
                title=%(title)s,picked_by=%(picked_by)s,date_watched=%(date_watched)s,
                description=%(description)s,fav_quote=%(fav_quote)s,comments=%(comments)s,
                updated_at=NOW() WHERE id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    def like(cls,data):
        query = """
                INSERT INTO likes (user_id, movie_id)
                VALUES (%(user_id)s, %(movie_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM movies WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all_users_movies(cls):
        query = """SELECT * FROM movies
                   JOIN users
                   ON users.id = movies.user_id
                """
        results = connectToMySQL(db).query_db(query)
        print(results)
        movies = []
        for row in results:
            movie = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name':row['first_name'],
                'last_name': row['last_name'],
                'username': row['username'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            movie.user = User(user_data)
            movies.append(movie)
        return movies
    

    @staticmethod
    def validate_movie(data):
        is_valid = True
        if len(data['title']) < 2:
            is_valid = False
            flash(" Uh uh uh! You didn't fill out the Movie!", "movie")
        if len(data['picked_by']) < 3:
            is_valid = False
            flash(" Uh uh uh! You didn't say who picked it!", "movie")
        if len(data['description']) < 2 :
            is_valid = False
            flash("Uh uh uh! Description must be filled out!", "movie")
            is_valid = False
        if data['date_watched'] == "":
            is_valid = False
            flash("Enter a date!", "movie")
        return is_valid


