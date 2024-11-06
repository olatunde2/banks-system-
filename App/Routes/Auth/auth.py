from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt, 
    get_jwt_identity
)
from flask_jwt_extended import current_user
from App.Models.Auth.user import TokenBlocklist, User


auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()
    user = User.get_user_by_username(username= data.get('username'))
    
    if user is not None:
        return jsonify({"message": "Username already exists"}), 409
    
    
    new_user = User(
        username=data.get('username'), 
        email=data.get('email')
    )
    new_user.set_password(password=data.get('password'))
    new_user.save()
    
    return jsonify({"message": "User registered successfully"}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_user_by_username(username=data.get('username'))
    
    if user and (user.check_password(password=data.get('password'))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)
        
        return jsonify(
            {
                "message": "Logged in successfully",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token
                }
            }
        ), 200
    
    
    return jsonify({"error": "Invalid credentials"}), 400

@auth.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    return jsonify({"message": current_user.username, "email": current_user.email}), 200

@auth.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200


@auth.route('/logout', methods=['GET'])
@jwt_required(verify_type=False)
def logout():
    jwt = get_jwt()
    jti = jwt['jti']
    token_type = jwt['type']
    token = TokenBlocklist(jti=jti)
    token.save()
    return jsonify({"message": f"{token_type} token revoked successfully"}), 200