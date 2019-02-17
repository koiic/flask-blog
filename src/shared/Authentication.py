import os
from functools import wraps

import jwt
import datetime
from flask import json, Response, request, g
from dotenv import load_dotenv
from pathlib import Path  # python3 only

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
from ..models.UserModel import UserModel

class Auth():
	""" Auth module for user authentication"""

	@staticmethod
	def generate_token(_user_id):
		""" Method to generate token """
		try:
			payload = {
				'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
				'iat': datetime.datetime.utcnow(),
				'sub': _user_id
			}
			return jwt.encode(
				payload,
				os.getenv('JWT_SECRET_KEY'),
				'HS256'
			).decode("utf-8")
		except Exception as e:
			raise e
			# response_message = {
			# 	'mimetype': "application/json",
			#     'response': {'error': 'error in generating user token'},
			#     'status': 400
			# }
			# return Response(json.dumps(response_message))


	@staticmethod
	def decode_token(token):
		"""Method to decode token"""
		response = {'data': {}, 'error': {}}
		try:
			payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), verify=False,   algorithms=['HS256'])
			response['data'] = {'user_id': payload['sub']}
			return response
		except jwt.ExpiredSignatureError as e:
			response['error'] = {'message': 'token expired, please try logging in again'}
			return response
		except jwt.InvalidTokenError as e:
			response['error'] = {'message': e.args}
			return response

	@staticmethod
	def auth_required(func):
		"""Auth decorator"""
		@wraps(func)
		def decorated_auth(*args, **kwargs):
			if 'Authorization' not in request.headers:
				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'No authentication token, login to be authenticate'}),
					status=400
				)
			token = request.headers.get('Authorization')
			print('======>>>>payload', token.split(' ')[1])

			data = Auth.decode_token(token.split(' ')[1])
			if data['error']:
				return Response(
					mimetype="application/json",
					response=json.dumps(data['error']),
					status=400
				)
			print('>>>>>>>', data)
			user_id = data['data']['user_id']
			check_user = UserModel.get_single_user(user_id)
			if not check_user:
				return Response(
					mimetype="application/json",
					response=json.dumps({'error': 'user does not exist, invalid token'}),
					status=400
				)
			g.user = {'id': user_id}
			return func(*args, **kwargs)
		return decorated_auth
