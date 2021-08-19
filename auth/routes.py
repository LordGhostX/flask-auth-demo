import time
from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from itsdangerous import JSONWebSignatureSerializer
from auth import app, db
from auth.models import User, Blacklist
from auth.utils import hash_password, verify_bcrypt

basic_auth = HTTPBasicAuth()
bearer_auth = HTTPTokenAuth(scheme="Bearer")
token_serializer = JSONWebSignatureSerializer(app.config["SERIALIZER_TOKEN"])


@basic_auth.verify_password
def verify_basic_auth(username, password):
    username = username.lower()
    user = User.query.get(username)
    if user and verify_bcrypt(password, user.password):
        return user


@bearer_auth.verify_token
def verify_bearer_auth(token):
    try:
        token_info = token_serializer.loads(token)
        if time.time() >= token_info["expiration"]:
            return False
    except:
        return False

    if Blacklist.query.get(token) is not None:
        return False

    user = User.query.get(token_info["username"])
    if user is not None:
        return user


@app.route("/", methods=["GET", "POST"])
def home_route():
    return "Hello World"


@app.route("/register/", methods=["POST"])
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


@app.route("/login/", methods=["POST"])
@basic_auth.login_required
def login():
    user = basic_auth.current_user()
    token_info = {
        "username": user.username,
        "expiration": int(time.time()) + app.config["TOKEN_EXPIRATION"]
    }
    token = token_serializer.dumps(token_info).decode("utf-8")

    return jsonify({
        "msg": "successfully authenticated user",
        "data": {
            "auth_token": token
        }
    }), 200


@app.route("/dashboard/", methods=["GET"])
@bearer_auth.login_required
def dashboard():
    user = bearer_auth.current_user()
    return jsonify({
        "msg": "successfully requested user info",
        "data": {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }), 200


@app.route("/logout/", methods=["GET"])
@bearer_auth.login_required
def logout():
    token = request.headers["Authorization"].split()[1]
    db.session.add(Blacklist(token=token))
    db.session.add()

    return jsonify({
        "msg": "successfully invalidated token",
        "data": None
    }), 200
