from flask import Flask, render_template, session, request, redirect, url_for, flash
import mysql.connector
import pymongo
from functools import wraps
from datetime import date
import app.lib.sql_db_init as sql_db_init
import app.lib.db_migrate as nosql_methods
import app.lib.forms as forms
import app.lib.db_methods as db_methods

# code to create the flask app instance
app = Flask(__name__)
app.config["DB_STATUS"] = ""
app.config["SECRET_KEY"] = "secret_key"

# default db type is sql
db_type = "sql"

# empty sql db created
sql_db = {
    "user": "admin",
    "password": "password",
    "database": "sql_imse",
    "host": "sql",
    "port": "8008",
}
db = mysql.connector.connect(**sql_db)

# empty mongogb db created and initialized
mongo_user = pymongo.MongoClient("mongodb://user:password@mongo:27017/")
mongo_db = mongo_user["mongo_imse"]
nosql_methods.reset_nosql(mongo_db)


def db_check(f):
    # check db status
    @wraps(f)
    def wrap(*args, **kwargs):
        if app.config["DB_STATUS"] == "":
            flash('Databases are not yet initialized. Please continue towards database reset page.', 'danger')
            return redirect(url_for('reset_db'))
        return f(*args, **kwargs)

    return wrap


def login_check(f):
    # check user login status
    @wraps(f)
    def wrap(*args, **kwargs):
        if not session.get('login_status'):
            flash('Currently not logged in. Please continue towards login page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return wrap


@app.route("/")
def index():
    if app.config["DB_STATUS"] == "":
        session.clear()
        return render_template("reset_db.html", title="Reset DBs")
    elif session.get("login_status"):
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route("/reset_db")
def reset_db():
    if app.config["DB_STATUS"] == "":
        app.config["DB_STATUS"] = "sql"
        sql_db_init.sql_empty_db(db)
        sql_db_init.sql_create_tables(db)
        sql_db_init.sql_insert_data(db)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("home"))
    

@app.route("/migrate_db")
@db_check
@login_check
def migrate_db():
    # migrate db page
    if app.config["DB_STATUS"] == "sql":
        app.config["DB_STATUS"] = "nosql"
        nosql_methods.migrate_db(db, mongo_db)
        sql_db_init.sql_empty_db(db)
        flash("Database migrated to nosql - mongo successfully.", "success")
        return redirect(url_for("home"))
    else:
        flash("Database is already migrated to nosql - mongo.", "danger")
        return redirect(url_for("home"))
    

# Saksham use case 1 -create account---------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    # register page
    form = forms.RegisterForm
    if form.validate_on_submit():
        user = db_methods.get_user_by_email(db, mongo_db, form.user_email.data)
        if user.user_email.data:
            flash("User with this email already exists. Please enter another email address.", "danger")
            return render_template("register.html", form=form, title="Register")
        else:
            db_methods.create_user(form.user_fullname.data, form.user_email.data, form.password.data)
            flash("User created successfully. Please login.", "success")
            return redirect(url_for("login"))
        
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # login page
    form = forms.LoginForm
    if form.validate_on_submit():
        user = db_methods.get_user_by_email(db, mongo_db, form.user_email.data, db_type)
        if user and user["password"] == form.password.data:
            session["login_status"] = True
            session["user_id"] = user["user_id"]
            session["full_name"] = user["full_name"]
            session["user_email"] = user["email"]
            session["DB_STATUS"] = app.config["DB_STATUS"]
            return redirect(url_for("home"))
            
        else:
            flash("Invalid username or password. Please try again.", "danger")
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
@login_check
def logout():
    # logout page
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/home")
@login_check
@db_check
def home():
    # home page
    return render_template("home.html", title="Home")


@app.route("/user_profile/<user_id>", methods=["GET", "POST"])
@login_check
@db_check
def user_profile(user_id):
    # user profile page
    # TODO: complete user profile page
    user_data = db_methods.get_user(db, mongo_db, user_id, db_type)
    return render_template("user_profile.html", title="User Profile", user_data=user_data)


@app.route("/attractions")
@login_check
@db_check
def attractions():
    # all attractions page
    attractions_data = db_methods.get_all_attractions(db, mongo_db, db_type)
    images = url_for('static', filename='images/img1.jpg')
    return render_template("attractions.html", title="Attractions", attractions_data=attractions_data, images=images)


@app.route("/attractions/<attraction_id>")
@login_check
@db_check
def attraction(attr_id):
    # specific attraction page
    attraction_data = db_methods.get_attraction(db, mongo_db, attr_id, db_type)
    image = url_for('static', filename=f'images/{attr_id}.jpg')
    return render_template("attraction.html", title=attraction_data["attr_name"], attraction_data=attraction_data, image=image)


# Saksham use case 2 -mark attraction as visited---------------------------------------------------------
@app.route("/attraction/<attraction_id>/mark_visited", methods=["GET", "POST"])
@login_check
@db_check
def mark_visited(attraction_id):
    # mark attraction as visited
    if attraction:
        visit_date = date.today()
        db_methods.mark_visited(db, mongo_db, session["user_id"], attraction_id, visit_date, db_type)
        return redirect(url_for("/attraction/<attraction_id>", attraction_id=attraction_id))


@app.route("/agencies")
@login_check
@db_check
def agencies():
    # all agencies page
    agencies_data = db_methods.get_all_agencies(db, mongo_db, db_type)
    return render_template("agencies.html", title="Agencies", agencies_data=agencies_data)


@app.route("/agency/<agency_id>")
@login_check
@db_check
def agency(agency_id):
    # specific agency page
    agency_data = db_methods.get_agency(db, mongo_db, agency_id, db_type)
    return render_template("agency.html", title="Agency", agency_data=agency_data)


@app.route("/agency/<agency_id>/tours")
@login_check
@db_check
def tours(agency_id):
    # a specific agency's all tours page
    tours_data = db_methods.get_all_tours(db, mongo_db, agency_id , db_type)
    return render_template("tours.html", title="Tours", tours_data=tours_data)


@app.route("/agency/<agency_id>/tours/<tour_id>")
@login_check
@db_check
def tour(tour_id):
    # specific tour page
    tour_data = db_methods.get_tour(db, mongo_db, tour_id, db_type)
    return render_template("tour.html", title="Tour", tour_data=tour_data)


# Mariam use case 1 -create a booking---------------------------------------------------------
@app.route("/tour/<tour_id>/create_booking", methods=["GET", "POST"])
@login_check
@db_check
def create_booking(tour_id):
    # create booking
    form = forms.BookingForm
    if form.validate_on_submit():
        db_methods.create_booking(db, mongo_db, session["user_id"], tour_id, form, db_type)
        flash("Booking created successfully.", "success")
        return redirect(url_for("home"))
    return render_template("create_booking.html", title="Create Booking", form=form)


# Mariam use case 2 -follow a user---------------------------------------------------------
@app.route("/follow/<followee_id>", methods=["GET", "POST"])
@login_check
@db_check
def follow(followee_id):
    # follow a user
    if followee_id:
        db_methods.follow(db, mongo_db, session["user_id"], followee_id, db_type)
        flash("You are now following this user.", "success")
        return redirect(url_for("home"))


@app.route("/bookings/<user_id>")
@login_check
@db_check
def bookings(user_id):
    # a user's bookings page
    bookings_data = db_methods.get_bookings(db, mongo_db, user_id, db_type)
    return render_template("booking.html", title="Bookings", bookings_data=bookings_data)
