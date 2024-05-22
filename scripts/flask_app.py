from flask import Flask, jsonify, request
from flask_cors import CORS
from db_manager import db_manager


app = Flask(__name__)
CORS(app)


@app.route("/login", methods=["POST"])
def login_route() :
    if request.method == "POST" :
        response = request.json
        username = response["username"]
        psswd = response["password"]
        
        if db_manager.authenticate_user(username, psswd) :
            return jsonify({
                "Status": "Success",
                "Response": "Valid user"
            }), 200
            
        else :
            return jsonify({
                "Status": "Failure",
                "Response": "Wrong username or password"
            }), 401
            
            
@app.route("/stream")
def stream_route() :
    pass