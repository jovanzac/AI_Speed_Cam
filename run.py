from dotenv import load_dotenv
load_dotenv(override=True)

from scripts.main import SpeedCam
from scripts.yolo_detection import detector
from scripts.bytetrack_tracker import tracker
from scripts.temp_speed_tracking import speed_estimator
from scripts.db_manager import db_manager


if __name__ == "__main__" :
    ai_cam = SpeedCam(detector=detector, tracker=tracker, speed_estimator=speed_estimator, db_manager=db_manager)
    ai_cam.display_vid_n_predict(speed_engine=True)