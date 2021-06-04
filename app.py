import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for )
from flask_pymongo import PyMongo 
from bson.objectid import ObjectId 
from werkzeug.security import generate_password_hash, check_password_hash
#import env package so it can be seen on Heroku. Otherwise errors due to gitignore. 
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
        # this checks if a username already exists in the db
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

        # now put the user into "session" cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")









if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")),debug=True)