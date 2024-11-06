from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from App.Models.Auth.user import User
from App.Routes.schemas import UserSchema



user_bp = Blueprint('user', __name__)

@user_bp.route('/all', methods = ['GET'])
@jwt_required()
def get_all_user():
    
    claims = get_jwt()
    
    if claims.get('is_admin') == True:
        page = request.args.get('page', default=1, type = int)
        per_page = request.args.get('per_page', default=10, type = int)
        
        user = User.query.paginate(
            page = page,
            per_page = per_page,
            error_out = False
        )
        
        result = UserSchema(many = True).dump(user.items)
        
        return jsonify({
            'users': result,
            
        }), 200
    
    return jsonify({"message": "Access denied"}), 401