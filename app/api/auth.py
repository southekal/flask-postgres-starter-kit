from flask import (
	Blueprint, 
	Flask, 
	jsonify,
	request
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, 
    jwt_optional,
    jwt_required
)
from flask_restful import (
	Api,
	Resource
)

from log_config.custom_logger import logger


api_auth = Blueprint('auth_api', __name__, url_prefix='/api/v1')
api = Api(api_auth)


class LoginHandler(Resource):
	def post(self):
		if not request.is_json:
			return ({"msg": "Missing JSON in request"}), 400

		email = request.json.get('email', None)
		password = request.json.get('password', None)
		if not email:
			return ({"msg": "missing email"}), 400
		if not password:
			return ({"msg": "missing password"}), 400

		if email != 'test@example.com' or password != 'tester++':
			return ({"msg": "bad email or password"}), 401

		access_token = create_access_token(identity=email)
		return {"access_token": access_token, "email": email}, 200
	
api.add_resource(LoginHandler, '/login')


class Settings(Resource):
	@jwt_required
	def post(self):
		logger.info(request.json)
		return {"msg": "success"}
	
api.add_resource(Settings, '/settings')




