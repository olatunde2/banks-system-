from flask import Flask, jsonify
from App.Models.extensions import db, jwt
from App.Routes.Users.routes import main  
from App.Routes.Auth.auth import auth    
from App.Routes.Users.users import user_bp as user  
from App.Models.Auth.user import TokenBlocklist, User  
from config import config  

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_prefixed_env(config[config_name])
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints with unique prefixes
    app.register_blueprint(main, url_prefix='/api/v1/main')
    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(user, url_prefix='/api/v1/user')
    
    # load user
    
    @jwt.user_lookup_loader
    def user_lookup(jwt_headers, jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(username=identity).one_or_none()
    
    # additional claims
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 'admin':
            return {'is_admin': True}
        return {'is_admin': False}
    
    # jwt error handlers
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            'message': 'Token has expired',
            'error': 'token_expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'message': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'message': 'Request does not contain an access token',
            'error': 'authorization_required'
        }), 401
        
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
        return token is not None
    

    return app
