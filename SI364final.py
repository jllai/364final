###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
import os
import requests
import json
import datetime
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

# Imports for login management
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from requests_oauthlib import OAuth2Session # If you haven't, need to pip install requests_oauthlib
from requests.exceptions import HTTPError

api_key = "ba3d19df0d9a631402140827c45d7b76"

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # So you can use http, not just https
basedir = os.path.abspath(os.path.dirname(__file__))


## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://Jamie@localhost:5432/SI364finaljllai" # TODO: May need to change this, Windows users -- probably by adding postgres:YOURTEXTPW@localhost instead of just localhost. Or just like you did in section or lecture before! Everyone will need to have created a db with exactly this name, though.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['HEROKU_ON'] = os.environ.get('HEROKU')

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

# Using shell
def make_shell_context():
    return dict( app=app, db=db, Videos=Videos, Channel=Channel)
# Add function use to manager
manager.add_command("shell", Shell(make_context=make_shell_context))

# OAuth configuration -- code lifted from Lecture 13
class Auth:
    """Google Project Credentials"""
    CLIENT_ID = ('696837306131-q8s3csk0sa0t5b3dhrof60beid7o87he.apps.googleusercontent.com') # Keep the parentheses in THIS line!
    CLIENT_SECRET = '8g-p5lZcA1beXdJxQ9XUeuE7'
    REDIRECT_URI = 'https://si364finaljllai.herokuapp.com' # Our (programmer's) decision
    # URIs determined by Google, below
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    SCOPE = ['profile', 'email'] # Could edit for more available scopes -- if reasonable, and possible without $$


class Config:
    """Base config"""
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "something secret"


class DevConfig(Config):
    """Dev config"""
    DEBUG = True
    USE_RELOADER = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/oauthex2" # TODO: Need to create this database or edit URL for your computer
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class ProdConfig(Config):
    """Production config"""
    DEBUG = False
    USE_RELOADER = True
    SQLALCHEMY_DATABASE_URI = "postgresql://Jamie@localhost/oauthex2_prod" # If you were to run a different database in production, you would put that URI here. For now, have just given a different database name, which we aren't really using.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# To set up different configurations for development of an application
config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
    }

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session( # make OAuth request
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

# Set up association Table between artists and albums
actors_movies = db.Table('actors_movies',db.Column('actor_id',db.Integer, db.ForeignKey('actors.id')),db.Column('movie_id',db.Integer, db.ForeignKey('movies.id')))
users_movies = db.Table('users_movies',db.Column('movie_id',db.Integer, db.ForeignKey('movies.id')),db.Column('user_id',db.Integer, db.ForeignKey('users.id')))
users_actors = db.Table('users_actors',db.Column('actor_id',db.Integer, db.ForeignKey('actors.id')),db.Column('user_id',db.Integer, db.ForeignKey('users.id')))
users_directors = db.Table('users_directors',db.Column('director_id',db.Integer, db.ForeignKey('directors.id')),db.Column('user_id',db.Integer, db.ForeignKey('users.id')))

######################################
########      HELPER FXN      ########
######################################
def get_movie_info(movie):
    if type(movie) == str:
        base_url = 'https://api.themoviedb.org/3/search/movie?query='
        inp = movie + '&api_key=' + api_key
    elif type(movie) == int:
        movie = str(movie)
        base_url = 'https://api.themoviedb.org/3/movie/'
        inp = movie + '?api_key=' + api_key
    results = requests.get(base_url + inp)
    json_file = json.loads(results.text)
    return json_file

def get_cast(movie):
    movie = str(movie)
    base_url = 'https://api.themoviedb.org/3/movie/'
    inp = movie + '/credits?api_key=' + api_key
    results = requests.get(base_url + inp)
    json_file = json.loads(results.text)
    return json_file

def get_person_info(person):
    if type(person) == str:
        base_url = 'https://api.themoviedb.org/3/search/person?query='
        inp = person + '&api_key=' + api_key
    elif type(person) == int:
        person = str(person)
        base_url = 'https://api.themoviedb.org/3/person/'
        inp = person + '?api_key=' + api_key
    results = requests.get(base_url + inp)
    json_file = json.loads(results.text)
    return json_file

def get_person_credits(person):
    person = str(person)
    base_url = 'https://api.themoviedb.org/3/person/'
    inp = person + '/movie_credits?api_key=' + api_key
    results = requests.get(base_url + inp)
    json_file = json.loads(results.text)
    return json_file

def get_or_create_movie(id):
    m = Movie.query.filter_by(tmdb_id=id).first()
    if m:
        return m
    else:
        id = int(id)
        movie = get_movie_info(id)
        cast = get_cast(id)
        for c in cast['crew']:
            if c['department'] == 'Directing':
                director = get_or_create_director(c['name'], c['id'])
                break
        m = Movie(title=movie['title'], rating=movie['vote_average'], desc=movie['overview'], tmdb_id=movie['id'], director_id=director.id)
        db.session.add(m)
        db.session.commit()
        current_user.movies.append(m)
        return m

def get_or_create_actor(id):
    a = Actor.query.filter_by(id=id).first()
    if a:
        return a
    else:
        id = int(id)
        person = get_person_info(id)
        a = Actor(name=person['name'], tmdb_id=person['id'], bio=person['biography'])
        movies = get_person_info(person['name'])
        for movie in movies['results'][0]['known_for']:
            m = get_or_create_movie(movie['id'])
            a.movies.append(m)
        db.session.add(a)
        db.session.commit()
        current_user.actors.append(a)
        return a

def get_or_create_director(name, tmdb_id):
    d = Director.query.filter_by(name=name).first()
    if d:
        return d
    else:
        person = get_person_info(tmdb_id)
        d = Director(name=name, tmdb_id=tmdb_id, bio=person['biography'])
        current_user.directors.append(d)
        db.session.add(d)
        db.session.commit()
        return d

##################
##### MODELS #####
##################

## User-related Models
class User(db.Model, UserMixin):
    __tablename__ = "users" # This was built to go with Google specific auth
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True) # come from google
    avatar = db.Column(db.String(200)) # from google
    tokens = db.Column(db.Text) # secure access from google
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow()) # created on my app at a certain time; user will be saved
    movies = db.relationship('Movie',secondary=users_movies,backref=db.backref('movies',lazy='dynamic'),lazy='dynamic')
    actors = db.relationship('Actor',secondary=users_actors,backref=db.backref('actors',lazy='dynamic'),lazy='dynamic')
    directors = db.relationship('Director',secondary=users_directors,backref=db.backref('directors',lazy='dynamic'),lazy='dynamic')

## DB load function
## Necessary for behind the scenes login manager that comes with flask_login capabilities! Won't run without this.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    desc = db.Column(db.String)
    rating = db.Column(db.String)
    tmdb_id = db.Column(db.Integer, unique=True)
    saved = db.Column(db.Boolean)
    personal_rating = db.Column(db.Integer)

    director_id = db.Column(db.Integer, db.ForeignKey("directors.id"))

    def __repr__(self):
        return "{}".format(self.title)

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    tmdb_id = db.Column(db.Integer, unique=True)
    bio = db.Column(db.String)
    movies = db.relationship('Movie',secondary=actors_movies,backref=db.backref('actors',lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return "{}".format(self.name)

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    tmdb_id = db.Column(db.String)
    bio = db.Column(db.String)
    movies = db.relationship('Movie',backref='Director')
    saved = db.Column(db.Boolean)

    def __repr__(self):
        return "{}".format(self.name)

###################
###### FORMS ######
###################
class SearchForm(FlaskForm):
    movie = StringField("What movie are you looking for?")
    actor = StringField("What actor would you like to look up?")
    director = StringField("What director would you like to look up?")
    submit = SubmitField('submit')

    def validate_actor(field, self):
        if ' ' not in field.data:
            raise ValidationError("Needs last name!")

class Save(FlaskForm):
    submit = SubmitField("Save")

class ButtonForm(FlaskForm):
    submit_del = SubmitField("Delete")
    personal_rating = StringField("Personal Rating, 1-10: ")
    submit_rating = SubmitField("Update")

    def validate_personal_rating(self, field):
        if float(field.data) < 0 or float(field.data) > 10:
            raise ValidationError(message="Rating outside of range!")


#######################
###### VIEW FXNS ######
#######################
## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



# Will ask for actor, director, or movie, and render templates for respective objects as well as use get_or_create helper functions to make each object that is submitted
@app.route('/', methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit() and form.actor.data == '':
        save_form = Save()
        movie_info = get_movie_info(form.movie.data)
        return render_template('movie_results.html', movies=movie_info['results'], form=save_form)
    elif request.args and request.args.get('movie') == None:
        print(request.args.get('movie'))
        save_form = Save()
        actor_info = get_person_info(request.args.get('actor'))
        return render_template('actor_results.html', actors=actor_info['results'], form=save_form)
    else:
        flash("***Cannot fill in both search forms!***")

    return render_template('index.html', form=form)

#renders template to show all actors that you follow with a link that shows all their movies

@app.route('/movie/<id>', methods=['GET','POST'])
def movie_results(id):
    movie = get_or_create_movie(id)
    movie.saved = True
    d = Director.query.filter_by(id=movie.director_id).first()
    d.saved = True
    flash("Successfully saved")
    return redirect(url_for('all_movies'))

# renders template to show all movies you save and their scores
@app.route('/all_movies', methods=['GET', 'POST'])
def all_movies():
    form = ButtonForm()
    movies = current_user.movies.all()
    return render_template('all_movies.html',movies=movies, form=form)

@app.route('/actor/<id>', methods=['GET','POST'])
def actor_results(id):
    get_or_create_actor(id)
    flash("Successfully saved")
    return redirect(url_for('all_actors'))

@app.route('/all_actors', methods=['GET', 'POST'])
def all_actors():
    actors = current_user.actors.all()
    return render_template('all_actors.html',actors=actors)

# renders template to show all directors you follow with a link to show all their movies
@app.route('/all_directors', methods=['GET', 'POST'])
def all_directors():
    directors = current_user.directors.all()
    return render_template('all_directors.html',directors=directors)

# updates your personal rating of the movie
@app.route('/update/<movie>',methods=["GET","POST"])
def update(movie):
    form = ButtonForm()
    if form.validate_on_submit():
        personal_rating = form.personal_rating.data
        m = Movie.query.filter_by(title=movie).first()
        m.personal_rating = personal_rating
        db.session.commit()
        flash("Updated rating of " + movie)
        return redirect(url_for('all_movies'))

    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash(str(errors))

    return redirect(url_for('all_movies'))
# deletes the movie from your saved movies
@app.route('/delete/<movie>',methods=["GET","POST"])
def delete(movie):
    m = Movie.query.filter_by(title=movie).first()
    db.session.delete(m)
    flash("Successfully deleted {}".format(m))
    return redirect(url_for('all_movies'))



#OAuth stuff
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth() # login with google
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='online')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)

@app.route('/gCallback')
def callback():
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args: # Good Q: 'what are request.args here, why do they matter?'
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    # print(request.args, "ARGS")
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            # print("SUCCESS 200") # For debugging/understanding
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                # print("No user...")
                user = User()
                user.email = email
            user.name = user_data['name']
            # print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

## Code to run the application...
if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
    manager.run()
# Put the code to do so here!
