# app/routes.py
from flask import Blueprint, jsonify

# Create a Blueprint for the main routes

main = Blueprint('main', __name__)

@main.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})
