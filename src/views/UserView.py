from flask import request, Response, json, jsonify, Blueprint, g

from src.utilities.messages import custom_response
from ..models.UserModel import UserModel
from ..schemas.UserSchema import UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()

@user_api.route('/', methods=['POST'])
def create_user():
	""" Create a new user"""
	request_data = request.get_json()
	data = user_schema.load_object_into_schema(request_data, partial=False)
	#
	# if error:
	# 	return Response(custom_response(json.dumps(error), 400))

	# check if user exist
	already_existing_user = UserModel.get_single_user_by_email(data.get('email'))
	if already_existing_user:
		return Response(mimetype="application/json", response=json.dumps(custom_response('user already exist')), status=409)

	user = UserModel(data)
	user.save()

	user_data = user_schema.dump(user).data
	token = Auth.generate_token(user_data.get('id'))
	message = 'user created successfully',
	return Response(mimetype="application/json", response=json.dumps(custom_response(message, token)), status=200)


@user_api.route('/login', methods=['POST'])
def login():
	request_data = request.get_json()

	data = user_schema.load_object_into_schema(request_data, partial=True)

	# if error:
	# 	return Response(custom_response(json.dumps(error), 400))

	if not data.get('email') or not data.get('password'):
		return Response(mimetype="application/json", response=json.dumps(custom_response({'error': 'Email and Password required'})), status=400)

	user = UserModel.get_single_user_by_email(data.get('email'))

	if not user:
		return Response(mimetype="application/json", response=json.dumps(custom_response({'error': 'invalid credentials'})), status=400)

	if not user.check_hash(data.get('password')):
		return Response(mimetype="application/json", response=json.dumps(custom_response({'error': 'Invalid password'})), status=200)

	user_data = user_schema.dump(user).data
	token = Auth.generate_token(user_data.get('id'))
	message = "You have been logged in successfully"
	return Response(mimetype="application/json", response=json.dumps(custom_response(message, token)), status=200)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
	users = UserModel.get_all_users()
	all_users = user_schema.dump(users, many=True).data
	return Response(mimetype="application/json",response=json.dumps(custom_response("users fetched successfully", all_users)), status=200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_single_user(user_id):
	"""Get A single User"""
	user = UserModel.get_single_user(user_id)
	if not user:
		return Response(mimetype="application/json", response=json.dumps(custom_response('User not found')), status=404)

	single_user = user_schema.dump(user).data
	return Response(mimetype="application/json",  response=json.dumps(custom_response("user fetched successfully", single_user)), status=200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
	"""Update my user information"""

	request_data = request.get_json()
	data, error = user_schema.load_object_into_schema(request_data, partial=True)

	if error:
		return Response(mimetype="application/json", response=json.dumps(custom_response(error)), status=400)

	user = UserModel.get_single_user(g.user.get('id'))
	user.update(data)

	updated_user = user_schema.dump(user).data
	return Response(mimetype="application/json", response=json.dumps(custom_response('user updated successfully', updated_user)), status=200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete_single_user():
	"""Delete User Information """
	user = UserModel.deleteUser(g.user.get('id'))
	deleted_user = user_schema.dump(user).data
	return Response(mimetype="application/json", response=json.dumps(custom_response('user has been deleted', deleted_user)), status=204)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_my_info():
	""" Get my persnal information"""
	user = UserModel.get_single_user(g.user.get('id'))
	fetched_user = user_schema.dump(user).data
	return Response(mimetype="application/json", response=json.dumps(custom_response('your info is fetched successfully', fetched_user)), status=200)
