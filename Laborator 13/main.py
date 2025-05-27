from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token,
    get_jwt_identity, jwt_required,
    get_jwt
)
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'hftghjk67$0%hh##'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


users = {
    'user1': {'password': 'parola1', 'role': 'admin'},
    'user2': {'password': 'parola2', 'role': 'owner'},
    'user3': {'password': 'parolaX', 'role': 'owner'}
}
invalid_tokens = set()

@app.route('/auth', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)

    if user and user['password'] == password:
        access_token = create_access_token(
            identity = username,
            additional_claims = {'role': user['role']}
        )
        return jsonify(access_token=access_token), 200
    return jsonify(msg = 'Invalid username or password'), 401

@app.route('/auth/jwtStore', methods=['GET'])
@jwt_required()
def validate():
    jwt_data = get_jwt()
    jti = jwt_data['jti']
    if jti in invalid_tokens:
        return jsonify(msg = 'Token invalidated'), 404

    identity = get_jwt_identity()
    return jsonify(username = identity, role = jwt_data.get('role')), 200

@app.route('/auth/jwtStore', methods=['DELETE'])
@jwt_required()
def logout():
    jwt_data = get_jwt()
    jti = jwt_data['jti']
    invalid_tokens.add(jti)
    return jsonify(msg = 'Logged out with success.'), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')