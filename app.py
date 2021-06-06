import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for )
from flask_pymongo import PyMongo 
from bson.objectid import ObjectId 
from werkzeug.security import generate_password_hash, check_password_hash

# import env package so it can be seen on Heroku. Otherwise errors due to 
# gitignore. 

if os.path.exists("env.py"):
    import env

# app is the instance of Flask

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


# an instance of pymongo by adding a constructor method, so the app object communicates with the Mongo db. 

mongo =PyMongo(app)



@app.route("/")
@app.route("/get_homes")
def get_homes():
    homes = list(mongo.db.homes.find())
    return render_template("homes.html", homes=homes)


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        # this sequence checks if a username already exists in the db:
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # this will put the user into a "session" cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        #check if username exists in db 
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for('login'))

        else:   
            # if username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
        
    return render_template("login.html")



@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # this grabs the session user's username from db
    username =mongo.db.users.find_one({"username": session["user"]})["username"]
    # List the current ads to be filtered on the page
    homes = list(mongo.db.homes.find())
    if session["user"]:
        return render_template("profile.html", username=username, homes=homes)



@app.route("/logout")
def logout():
    # this removes user from session cookies
    flash("Thanks, you are now logged out. ")
    session.pop("user")
    return redirect(url_for("login"))



@app.route("/add_home", methods=["GET", "POST"])
def add_home():
    if request.method =="POST":
        by_owner = "on" if request.form.get("by_owner") else "off"
        home = {
            "category_name": request.form.get("category_name"),
            "list_title": request.form.get("list_title"),
            "list_description": request.form.get("list_description"),
            "list_bedrooms": request.form.get("list_bedrooms"),
            "list_price": request.form.get("list_price"),
            "sold_by": request.form.get("sold_by"),
            "sale_sold": request.form.get("sale_sold"),
            "created_by": session['user'],
            "list_image1" : request.form.get("list_image1"),
            "list_image2" : request.form.get("list_image2"),
            "list_image3" : request.form.get("list_image3")
            }
        mongo.db.homes.insert_one(home)
        flash("Your New Property Was Successfully Added.")
    categories= mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_home.html", categories=categories)
    

@app.route("/edit_home/<home_id>", methods =["GET", "POST"])
def edit_home(home_id):    
    if request.method =="POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "list_title": request.form.get("list_title"),
            "list_description": request.form.get("list_description"),
            "list_bedrooms": request.form.get("list_bedrooms"),
            "list_price": request.form.get("list_price"),
            "sold_by": request.form.get("sold_by"),
            "sale_sold": request.form.get("sale_sold"),
            "list_image1" : request.form.get("list_image1"),
            "list_image2" : request.form.get("list_image2"),
            "list_image3" : request.form.get("list_image3"),
            "created_by": session['user']
            }
        mongo.db.homes.update({"_id": ObjectId(home_id)},submit)
        flash("Property Successfully updated")
    categories= mongo.db.categories.find().sort("category_name", 1)
    home = mongo.db.homes.find_one({"_id":ObjectId(home_id)})
    categories= mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_home.html", home=home, categories=categories)
    

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),debug=True)