from scripts.main import SpeedCam
# from scripts.video_streaming import VidStream
from scripts.yolo_detection import Detection
from scripts.bytetrack_tracker import Tracker
from scripts.temp_speed_tracking import SpeedDetection
from scripts.db_manager import DbManager


detector = Detection()
tracker = Tracker()
speed_estimator = SpeedDetection()
db_manager = DbManager()
ai_cam = SpeedCam(detector=detector, tracker=tracker, speed_estimator=speed_estimator, db_manager=db_manager)
# ai_cam.dummy()
# streamer = VidStream(ai_cam)