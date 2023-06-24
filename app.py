import os
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_path=current_dir, instance_relative_config=True)
app.config['SECRET_KEY'] = 'XgSODQOM'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///user_credentials.db'
}


db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    book_id = db.Column(db.Integer)


class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return redirect("/index")
        else:
            flash("Something went wrong", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/index")
def index():
    books = Book.query.all()

    return render_template("index.html", books=books)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different username.", "error")
            return redirect("/signup")

        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! You can now login.", "success")
        return redirect("/index")

    return render_template("signup.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
