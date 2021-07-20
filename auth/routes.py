from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from auth import app, db
from auth.models import User
from auth.utils import hash_password, verify_bcrypt

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_basic_auth(username, password):
    username = username.lower()
    user = User.query.get(username)
    if user and verify_bcrypt(password, user.password):
        return user


@app.route("/")
def home_route():
    return "Hello World"


@app.route("/auth/register/", methods=["POST"])
def register():
    username = request.form.get("username", "")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    password = request.form.get("password", "")

    if "" in [username, password]:
        return jsonify({
            "msg": "username and password are required fields",
            "data": None
        }), 400

    if User.query.get(username) is not None:
        return jsonify({
            "msg": "this user profile already exists",
            "data": None
        }), 409

    user = User(username=username.lower(), first_name=first_name,
                last_name=last_name, password=hash_password(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg": "successfully created user profile",
        "data": None
    }), 201


@app.route("/auth/login/", methods=["POST"])
@basic_auth.login_required
def login():
    user = basic_auth.current_user()
    return user.username
