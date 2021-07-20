from flask import request, jsonify
from auth import app, db
from auth.models import User
from auth.utils import hash_password


@app.route("/")
def home_route():
    return "Hello World"


@app.route("/auth/register/", methods=["POST"])
def register_user():
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
