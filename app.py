import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for,
    jsonify)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
if os.path.exists("env.py"):
    import env


UPLOAD_FOLDER = 'static/img/'

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mongo = PyMongo(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# allowed file method


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# method to upload image to database


def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        # flash('Image successfully uploaded and displayed below')
        # return render_template('recipes.html', filename=filename)
        return filename

    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        # return redirect(request.url)

# routes


@app.route("/")
@app.route("/get_recipes")
def get_recipes():
    recipes = list(mongo.db.recipes.find())
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)
    for recipe in recipes:
        try:
            recipe["user_id"] = mongo.db.users.find_one(
                {"_id": recipe["user_id"]})["username"]
        except:
            pass
    return render_template("recipes.html", recipes=recipes,
        dropdown_recipes=recipes, cuisines=cuisines)



@app.route("/get_recipe_example")
def get_recipe_example():
    recipes = mongo.db.recipes

    offset = 1
    limit = 3

    starting_id = mongo.db.recipes.find().sort("_id", 1)
    last_id = starting_id[offset]['_id']

    recipes = mongo.db.recipes.find({'_id': {'$gte': last_id}}).sort("_id", 1).limit(limit)

    output = []

    for i in recipes:
        output.append({'recipe' : i['recipe_name']})

    next_url = '/get_recipe_example?limit=' + str(limit) + '&offset=' + str(offset + limit)
    prev_url = '/get_recipe_example?limit=' + str(limit) + '&offset=' + str(offset - limit)

    return jsonify({'result': output, 'prev_url': prev_url, 'next_url': next_url})

    #return render_template("get_recipe_example.html", recipes=recipes, prev=prev_url, next=next_url)




@app.route("/search_recipe", methods=["GET", "POST"])
def search_recipe():
    dropdown_recipes = list(mongo.db.recipes.find())
    query = request.form.get("query")
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)

    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes,
        dropdown_recipes=dropdown_recipes, cuisines=cuisines)


@app.route("/search_by_cuisine", methods=["GET", "POST"])
def search_by_cuisine():
    dropdown_recipes = list(mongo.db.recipes.find())
    query_cuisine = request.form.get("cuisine_name")
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)

    recipes = list(mongo.db.recipes.find(
        {"$text": {"$search": query_cuisine}})
        )
    return render_template("recipes.html", recipes=recipes, 
        dropdown_recipes=dropdown_recipes, cuisines=cuisines)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
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
                # find user that matches current session
                recipe["user_id"] = mongo.db.users.find_one(
                    {"_id": recipe["user_id"]})["username"]
            except:
                pass
        return render_template(
            "profile.html", username=username.capitalize(), recipes=recipes)

    return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":

        user = mongo.db.users.find_one({"username": session["user"]})
        new_recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": request.form.getlist("ingredients"),
            "prep_time": request.form.get("prep_time"),
            "file": upload_image(),
            "prep_steps": request.form.getlist("prep_steps"),
            "cook_time": request.form.get("cook_time"),
            "cuisine_name": request.form.get("cuisine_name"),
            "created_by": session["user"],
            "user_id": ObjectId(user["_id"])
            }
        mongo.db.recipes.insert_one(new_recipe)
        flash("Recipe Successfully Added!")
        return redirect(url_for("get_recipes"))

    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)
    return render_template("add_recipe.html", cuisines=cuisines)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
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

        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, update_recipe)
        flash("Recipe Successfully Updated")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    cuisines = mongo.db.cuisines.find().sort("cuisine_name", 1)
    return render_template("edit_recipe.html", recipe=recipe, cuisines=cuisines)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted")
    return redirect(url_for("get_recipes"))


@app.route("/get_cuisines")
def get_cuisines():
    cuisines = list(mongo.db.cuisines.find().sort("cuisine_name", 1))
    return render_template("cuisines.html", cuisines=cuisines)


@app.route("/add_cuisine", methods=["GET", "POST"])
def add_cuisine():
    if request.method == "POST":
        add_cuisine = {
            "cuisine_name": request.form.get("cuisine_name")
        }
        mongo.db.cuisines.insert_one(add_cuisine)
        flash("New Cuisine Added")
        return redirect(url_for("get_cuisines"))

    return render_template("add_cuisine.html")


@app.route("/edit_cuisine/<cuisine_id>", methods=["GET", "POST"])
def edit_cuisine(cuisine_id):
    if request.method == "POST":
        edit_cuisine = {
            "cuisine_name": request.form.get("cuisine_name")
        }
        mongo.db.cuisines.update({"_id": ObjectId(cuisine_id)}, edit_cuisine)
        flash("Cuisine Successfully Updated")
        return redirect(url_for("get_cuisines"))

    cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
    return render_template("edit_cuisine.html", cuisine=cuisine)


@app.route("/delete_cuisine/<cuisine_id>")
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({"_id": ObjectId(cuisine_id)})
    flash("Cuisine Successfully Deleted")
    return redirect(url_for("get_cuisines"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
# Remember to change debug to False before submitting project