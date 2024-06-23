from flask import Flask, jsonify, request, Response, render_template
from flask_cors import CORS
from scripts import db_manager, ai_cam


# app = Flask(__name__)
app = Flask(__name__, static_url_path='',
                  static_folder='dist',
                  template_folder='dist')
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)   
def not_found(e):   
  return app.send_static_file('index.html')


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
            
            
@app.route("/signup", methods=["POST"])
def signup_user() :
    if request.method == "POST" :
        response = request.json
        uid = response["uid"]
        name = response["name"]
        username = response["username"]
        psswd = response["password"]
        email = response["email"]
        phone_no = response["phone_no"]
        
        if db_manager.signup_user(uid, name, username, psswd, email, phone_no) :
            return jsonify(
                {
                    "Status": "Success",
                    "Response": "User created"
                }
            ), 200
            
        else :
            return jsonify(
                {
                    "Status": "Failure",
                    "Response": "User already exists"
                }
            ), 409
            
            
@app.route('/raw-video', methods=["GET"])
def raw_video_stream():
    if request.method == "GET" :
        return Response(ai_cam.yeild_processed_frames(speed_engine=False),mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route("/processed-video", methods=["GET"])
def processed_video_stream() :
    if request.method == "GET" :
        return Response(ai_cam.yeild_processed_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    
    
@app.route("/plate-info", methods=["GET"])
def get_plate_info() :
    if request.method == "GET" :
        all_plates = db_manager.get_plates_from_mongo()
        plates = list(filter(lambda plate: plate["valid"], all_plates))
        
        return jsonify({
            "Status": "Success",
            "Response": plates
        }, 200)