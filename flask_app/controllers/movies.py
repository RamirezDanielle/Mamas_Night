from flask_app import app
from flask import Flask, request, render_template, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.movie import Movie


#bio page
@app.route('/about')
def about():
   return render_template('about_me.html')


#add movie page
@app.route('/enter/movie')
def enter():
   if 'user_id' not in session:
      return redirect('/')
   return render_template('add_movie.html')

# movie page
@app.route('/movies')
def movie_page():
   if 'user_id' not in session:
      return redirect('/')
   user_data = {
      'id':  session['user_id']
   }
   user = User.get_one(user_data)
   movies = Movie.get_all()
   return render_template('movie.html',movies=movies,user=user)

# all movies
@app.route('/all/movies')
def all_movies():
   if 'user_id' not in session:
      return redirect('/')
   user_data = {
      'id':  session['user_id']
   }
   user = User.get_one(user_data)
   movies = Movie.get_all_users_movies()
   return render_template('all_movies.html',movies=movies, user = user)

#add movie watched
@app.route('/submit/movie', methods=['POST'])
def new_movie():
   if 'user_id' not in session:
        return redirect('/logout')
   if not Movie.validate_movie(request.form):
      return redirect('/enter/movie')
   data = {
      'title': request.form['title'],
      'picked_by': request.form['picked_by'],
      'date_watched': request.form['date_watched'],
      'description' : request.form['description'],
      'fav_quote' : request.form['fav_quote'],
      'comments' : request.form['comments'],
      'user_id' : session['user_id'],
   }
   Movie.save(data)
   print(request.form)
   return redirect('/movies')




#update movie watched
@app.route('/update/movie', methods=['POST'])
def update_movie():
   if 'user_id' not in session:
        return redirect('/logout')
   # if not Movie.validate_movie(request.form):
   #    return redirect('edit_movie.html')
   data = {
      'id' : request.form['id'],
      'title': request.form['title'],
      'picked_by': request.form['picked_by'],
      'date_watched': request.form['date_watched'],
      'description' : request.form['description'],
      'fav_quote' : request.form['fav_quote'],
      'comments' : request.form['comments'],
   }
   Movie.update(data)
   print(request.form)
   return redirect('/movies')

#edit movie
@app.route('/edit/movies/<int:id>')
def edit_movie(id):
   if 'user_id' not in session:
      return redirect('/logout')
   edit=Movie.get_one(id)
   return render_template('edit_movie.html', edit=edit)



#delete movie
@app.route('/remove/movies/<int:id>')
def delete(id):
   if 'user_id' not in session:
      return redirect('/logout')
   data = {
      'id': id
   }
   Movie.delete(data)
   return redirect('/movies')