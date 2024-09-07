from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

user: dict = {
    "username": "lawsonredeye",
    "password": generate_password_hash("Iam groot")
    }

def login():
    username: str = "lawsonredeye" #request.form.get("username")
    password: str = "this is sparta" #request.form.get("password")
    if username == None:
        return jsonify({"error": "Missing username"}), 400
    if password == None:
        return jsonify({"error": "Missing password"}), 400
    # make call to database to fetch user data
    if check_password_hash(user["password"], password):
        token: str = str(uuid4())
        return jsonify({"message": "Success", "token": token}), 200
    else:
        return jsonify({"error": "Incorrect password"})
