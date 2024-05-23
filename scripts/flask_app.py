from flask import Flask, jsonify, request, Response, render_template
from flask_cors import CORS
from scripts import db_manager, ai_cam


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


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
            
            
@app.route('/raw-video', methods=["GET"])
def raw_video_stream():
    if request.method == "GET" :
        return Response(ai_cam.yeild_processed_frames(speed_engine=False),mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route("/processed-video", methods=["GET"])
def processed_video_stream() :
    if request.method == "GET" :
        return Response(ai_cam.yeild_processed_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')