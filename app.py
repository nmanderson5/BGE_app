from flask import Flask, render_template, request, redirect, session, url_for
from flask_scss import Scss
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, ForeignKey, Integer, or_, select, String, update
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from typing import List, Optional
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = "MtJ5F3"

# Configure session to not use cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///eggs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True



# Create the base class for our models
class Base(DeclarativeBase):
    pass


# Initialize the session and database connection
Session(app)
db = SQLAlchemy(app, model_class=Base)



# Database Model
class User(db.Model):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(24), unique=True)
    password_hash: Mapped[str] = mapped_column(String(64))
    
    egg: Mapped["Egg"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Recipe(db.Model):
    __tablename__ = "recipe_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(24))
    temps: Mapped[str] = mapped_column(String(24))
    entree: Mapped[str] = mapped_column(String(8))
    cook_method: Mapped[str] = mapped_column(String(8))
    source: Mapped[str] = mapped_column(String(120))
    meats: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Recipe(id={self.id!r}, name={self.name!r})"




class Egg(db.Model):
    __tablename__ = "egg_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    left_bot_acc: Mapped[str] = mapped_column(String(16), insert_default="Empty")
    right_bot_acc: Mapped[str] = mapped_column(String(16), insert_default="Empty")
    left_mid_acc: Mapped[str] = mapped_column(String(16), insert_default="Grid")
    right_mid_acc: Mapped[str] = mapped_column(String(16), insert_default="Grid")
    top_acc: Mapped[str] = mapped_column(String(16), insert_default="Empty")
    temp: Mapped[int] = mapped_column(insert_default=0)
    left_bot_food: Mapped[Optional[int]]
    right_bot_food: Mapped[Optional[int]]
    left_mid_food: Mapped[Optional[int]]
    right_mid_food: Mapped[Optional[int]]
    top_food: Mapped[Optional[int]]
    user_id = mapped_column(ForeignKey("user_table.id"))

    user: Mapped["User"] = relationship(back_populates="egg")

    def __repr__(self) -> str:
        return f"Egg(id={self.id!r}, temp={self.temp!r}, user_id={self.user_id!r})"


# Create the tables in the database
with app.app_context():
    db.create_all()


# Lists for dropdown menus
accessories = ["ConvEggtor", "Grid", "Vegetable Tray", "Baking Stone", "Griddle", "Wok"]
areas = ["Left Bottom", "Right Bottom", "Left Middle", "Right Middle", "Top"]



# Convert areas to field names
def area_acc(area):
    if area == "Left Bottom":
        return "left_bot_acc"
    elif area == "Left Middle":
        return "left_mid_acc"
    elif area == "Right Bottom":
        return "right_bot_acc"
    elif area == "Right Middle":
        return "right_mid_acc"
    elif area == "Top":
        return "top_acc"
    else:
        return None
    
def area_food(area):
    if area == "Left Bottom":
        return "left_bot_food"
    elif area == "Left Middle":
        return "left_mid_food"
    elif area == "Right Bottom":
        return "right_bot_food"
    elif area == "Right Middle":
        return "right_mid_food"
    elif area == "Top":
        return "top_food"
    else:
        return None

# Create a list of the names of the recipes currently on the Egg
def get_names(egg):
    names = {}
    r_0 = db.session.get(Recipe, egg.left_bot_food)
    if r_0:
        names["left_bot_food"] = r_0.name
    else:
        names["left_bot_food"] = None
    r_1 = db.session.get(Recipe, egg.right_bot_food)
    if r_1:
        names["right_bot_food"] = r_1.name
    else:
        names["right_bot_food"] = None
    r_2 = db.session.get(Recipe, egg.left_mid_food)
    if r_2:
        names["left_mid_food"] = r_2.name
    else:
        names["left_mid_food"] = None
    r_3 = db.session.get(Recipe, egg.right_mid_food)
    if r_3:
        names["right_mid_food"] = r_3.name
    else:
        names["right_mid_food"] = None
    r_4 = db.session.get(Recipe, egg.top_food)
    if r_4:
        names["top_food"] = r_4.name
    else:
        names["top_food"] = None
    return names



# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Routes
# Send a user to their dashboard or to login
@app.route("/", methods=["GET", "POST"])
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")


# Login user if username and password hash match database
@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return render_template("index.html")


# Register a new user by adding their information to the database
@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="User already exists!")
    else:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        new_egg = Egg(user_id=new_user.id)
        db.session.add(new_egg)
        db.session.commit()
        return redirect(url_for('dashboard'))


# Dashboard gets the user, their egg, and the names of the recipes on it
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" in session:
        user = db.session.scalar(select(User).where(User.username == session['username']))
        egg = user.egg
        name_list = get_names(egg)
        return render_template("dashboard.html", username=session['username'], accessories=accessories, areas=areas, egg=egg, name_list=name_list)
    return redirect(url_for('home'))


# Logout by removing user from the session
@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for('home'))


# Browse for recipes using the response on the search-form
@app.route("/browse", methods=["GET", "POST"])
def browse():
    if request.method == "POST":
        srch_term = request.form['term']
        srch_entree = str(request.form['entree'])
        srch_temp = request.form['temp']
        upper = str(int(srch_temp) + 25)
        lower = str(int(srch_temp) - 25)
        srch_method = request.form['cook_method']
        if srch_term:
            stmt = select(Recipe).where(and_(Recipe.name.like(f"%{srch_term}%"), Recipe.entree == srch_entree, Recipe.cook_method == srch_method, or_(Recipe.temps.like(f"%{upper}%"), Recipe.temps.like(f"%{srch_temp}%"), Recipe.temps.like(f"%{lower}%")))).order_by(Recipe.name)
        else:
            stmt = select(Recipe).where(and_(Recipe.entree == srch_entree, Recipe.cook_method == srch_method, or_(Recipe.temps.like(f"%{upper}%"), Recipe.temps.like(f"%{srch_temp}%"), Recipe.temps.like(f"%{lower}%")))).order_by(Recipe.name)
        results = db.session.scalars(stmt).all()
        return render_template("results.html", results=results, areas=areas)
    else:
        return render_template("browse.html")


# Search for recipes that match the current settings on the Egg
@app.route("/match_egg", methods=["GET"])
def match_egg():
    user = db.session.scalar(select(User).where(User.username == session['username']))
    egg = user.egg
    upper = str(egg.temp + 25)
    lower = str(egg.temp - 25)
    if egg.left_bot_acc == "ConvEggtor" and egg.right_bot_acc == "ConvEggtor":
        stmt = select(Recipe).where(Recipe.cook_method == "indirect", or_(Recipe.temps.like(f"%{egg.temp}%"), Recipe.temps.like(f"%{lower}%"), Recipe.temps.like(f"%{upper}%"))).order_by(Recipe.name)
    elif egg.left_bot_acc == "ConvEggtor" or egg.right_bot_acc == "ConvEggtor":
        stmt = select(Recipe).where(or_(Recipe.temps.like(f"%{egg.temp}%"), Recipe.temps.like(f"%{lower}%"), Recipe.temps.like(f"%{upper}%"))).order_by(Recipe.name).all()
    else:
        stmt = select(Recipe).where(Recipe.cook_method == "direct", or_(Recipe.temps.like(f"%{egg.temp}%"), Recipe.temps.like(f"%{lower}%"), Recipe.temps.like(f"%{upper}%"))).order_by(Recipe.name)
    results = db.session.scalars(stmt).all()
    return render_template("results.html", results=results, areas=areas)


# Add accessory
@app.route("/add_acc", methods=["POST"])
def add_acc():
    area = request.form.get("area")
    acc = request.form.get("accessory")
    if area not in areas or acc not in accessories:
        return redirect(url_for('dashboard'))
    user = db.session.scalar(select(User).where(User.username == session['username']))
    egg = user.egg
    field = area_acc(area)
    db.session.execute(update(Egg).where(Egg.id == egg.id).values({field: acc}))
    db.session.commit()
    return redirect(url_for('dashboard'))


# Add food to Egg
@app.route("/add_food", methods=["POST"])
def add_food():
    area = request.form.get("area")
    food = request.form .get("food")
    if area not in areas:
        return redirect(url_for('dashboard'))
    user = db.session.scalar(select(User).where(User.username == session['username']))
    egg = user.egg
    field = area_food(area)
    db.session.execute(update(Egg).where(Egg.id == egg.id).values({field: food}))
    db.session.commit()
    return redirect(url_for('dashboard'))


# Clear the Egg
@app.route("/clear", methods=["GET"])
def clear():
    user = db.session.scalar(select(User).where(User.username == session['username']))
    egg = user.egg
    egg.left_bot_acc = "Empty"
    egg.right_bot_acc = "Empty"
    egg.right_mid_acc = "Grid"
    egg.left_mid_acc = "Grid"
    egg.top_acc = "Empty"
    egg.temp = 0
    egg.left_bot_food = None
    egg.right_bot_food = None
    egg.left_mid_food = None
    egg.right_mid_food = None
    egg.top_food = None
    db.session.commit()
    return redirect(url_for('dashboard'))


# Set/change the temp on your egg
@app.route("/set_temp", methods=["POST"])
def set_temp():
    user = db.session.scalar(select(User).where(User.username == session['username']))
    egg = user.egg
    egg.temp = request.form['temp']
    db.session.commit()
    return redirect(url_for('dashboard'))



if __name__ in "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)