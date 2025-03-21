from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import secrets

secret_key = secrets.token_urlsafe()


app = Flask(__name__)

# setup the Flask jWt-extednded extension
app.config["JWT_SECRET_KEY"] = secret_key
jwt = JWTManager(app)


@app.route('/login', methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != 'test':
        return jsonify({'msg': "Bad username or password"}), 401
    access_token =  create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    app.run()