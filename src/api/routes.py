"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

def hashed_password(password: str ) -> str:
    encoded_password = password.encode("utf-8")
    hash_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
    return hash_password.decode("utf-8")

@api.route('/signup', methods=['POST'])
def new_user():
    response_body = {}
    data = request.get_json()
    required_data = ["email", "password"]
    for field in required_data:
        if field not in data:
            response_body =  "One or more fields are missed"
            return response_body, 400
    user = User(
        email = data["email"],
        password = hashed_password(data["password"]),
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    response_body = "Usuario creado!"

    return response_body, 201

@api.route('/login', methods=['POST'])
def handle_login():
    response_body = {}
    data = request.get_json()
    required_data = ["email", "password"]
    if not data:
        response_body = "Error in the json"
        return response_body, 400
    
    for field in required_data:
        if field not in data:
            response_body = "One or more fields are missed"
            return response_body, 400
    
    user = db.session.scalars(db.select(User).filter(
        User.email.ilike(data["email"]))).first()
    if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
        response_body["error"] = "Invalid email or password"
        return response_body, 401
    
    access_token = create_access_token (
        identity = str(user.id_user)
    )
    response_body = {
        "message" : "Login succesfull",
        "access_token" : access_token,
        "user_id" : user.id_user,
        "email" : user.email
    }
    return response_body, 200

@api.route('/private', methods=['GET'])
@jwt_required()
def handle_private():
    response_body = {}
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    response_body = {
        "user_id" : user.id_user,
        "email" : user.email
    }
    return response_body, 200



