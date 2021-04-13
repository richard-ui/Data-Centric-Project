import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mongo = PyMongo(app)


# decorator

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        #  user authentication set in place for more security

        if session.get('user'):
            existing_user = mongo.db.users.find_one(
                {"username": session['user']})
            if not existing_user["is_admin"]:
                return redirect(url_for("login"))
        else:
            return redirect(url_for("login"))

        return f(*args, **kwargs)
    return decorated_function


# routes


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    # find all recipes from mongodb
    recipes = list(mongo.db.recipes.find())
    # find all current cuisine types alphebetically
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)
    for recipe in recipes:
        try:
            # find username with same id in both users and recipes
            recipe["user_id"] = mongo.db.users.find_one(
                {"_id": recipe["user_id"]})["username"]
            # raise error if false
        except ValueError:
            pass
    return render_template("recipes.html", recipes=recipes,
                           dropdown_recipes=recipes, cuisines=cuisines)


# allows user to search by textbox
@app.route("/search_recipe", methods=["GET", "POST"])
def search_recipe():
    dropdown_recipes = list(mongo.db.recipes.find())
    query = request.form.get("query")  # query textbox value
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)

    # find recipe from input
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes,
                           dropdown_recipes=dropdown_recipes,
                           cuisines=cuisines)


# allows user to search by dropdown list
@app.route("/search_by_cuisine", methods=["GET", "POST"])
def search_by_cuisine():
    # use dropdown list to allow users to search from dropdown list
    dropdown_recipes = list(mongo.db.recipes.find())
    query_cuisine = request.form.get("cuisine_name")
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)

    # query to search recipes
    recipes = list(mongo.db.recipes.find(
        {"$text": {"$search": query_cuisine}})
        )
    return render_template("recipes.html", recipes=recipes,
                           dropdown_recipes=dropdown_recipes,
                           cuisines=cuisines)


# register user into db
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # warning error
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # if passed, username, password will be inserted, aswell as inserting
        # is_admin to be set to false as they wont have access to admin rights
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "is_admin": False
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                session["is_admin"] = existing_user["is_admin"] or False

                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                     "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    recipes = list(mongo.db.recipes.find())
    if session["user"]:
        for recipe in recipes:
            try:
                # find username with same id in both users and recipes
                recipe["user_id"] = mongo.db.users.find_one(
                    {"_id": recipe["user_id"]})["username"]
            # raise error if false
            except ValueError:
                pass
        return render_template(
            "profile.html", username=username.capitalize(), recipes=recipes)

    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        # find user with session login
        user = mongo.db.users.find_one({"username": session["user"]})
        new_recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.getlist("ingredients"),
            "prep_time": request.form.get("prep_time"),
            "file": request.form.get("recipe_image_url"),
            "prep_steps": request.form.getlist("prep_steps"),
            "cook_time": request.form.get("cook_time"),
            "cuisine_name": request.form.get("cuisine_name"),
            "created_by": session["user"],
            "user_id": ObjectId(user["_id"])
            }
        # use insert one command to insert the dictionary form into the
        # database
        mongo.db.recipes.insert_one(new_recipe)
        flash("Recipe Successfully Added!")
        return redirect(url_for("get_recipes"))

    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)
    return render_template("add_recipe.html", cuisines=cuisines)


# edit recipe
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        # find user with same session
        user = mongo.db.users.find_one({"username": session["user"]})
        update_recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.getlist("ingredients"),
            "prep_time": request.form.get("prep_time"),
            "file": request.form.get("file"),
            "prep_steps": request.form.getlist("prep_steps"),
            "cook_time": request.form.get("cook_time"),
            "cuisine_name": request.form.get("cuisine_name"),
            "created_by": session["user"],
            "user_id": ObjectId(user["_id"])
        }
        # retrieves users id and updates recipes accordingly using the form
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, update_recipe)
        flash("Recipe Successfully Updated")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)
    return render_template("edit_recipe.html", recipe=recipe,
                           cuisines=cuisines)


# remove current recipe by id
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("get_recipes"))


# get list of cuisines
@app.route("/get_cuisines")
@login_required
def get_cuisines():
    # find and sort them alphebetically
    cuisines = list(mongo.db.cuisines.find().sort("cuisine_name", 1))
    return render_template("cuisines.html", cuisines=cuisines)


@app.route("/add_cuisine", methods=["GET", "POST"])
@login_required
def add_cuisine():
    if request.method == "POST":
        add_cuisine = {
            "cuisine_name": request.form.get("cuisine_name")
        }
        # insert one command to add new cuisine name
        mongo.db.cuisines.insert_one(add_cuisine)
        flash("New Cuisine Added")
        return redirect(url_for("get_cuisines"))

    return render_template("add_cuisine.html")


# edit current cuisine
@app.route("/edit_cuisine/<cuisine_id>", methods=["GET", "POST"])
@login_required
def edit_cuisine(cuisine_id):
    if request.method == "POST":
        edit_cuisine = {
            "cuisine_name": request.form.get("cuisine_name")
        }
        # update with form text field
        mongo.db.cuisines.update({"_id": ObjectId(cuisine_id)}, edit_cuisine)
        flash("Cuisine Successfully Updated")
        return redirect(url_for("get_cuisines"))

    cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
    return render_template("edit_cuisine.html", cuisine=cuisine)


# remove cuisine by id
@app.route("/delete_cuisine/<cuisine_id>")
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({"_id": ObjectId(cuisine_id)})
    flash("Cuisine Successfully Deleted")
    return redirect(url_for("get_cuisines"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)

# switch debug to false on deployment
