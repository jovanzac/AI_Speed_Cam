import cv2
from scripts.yolo_detection import Detection
from scripts.bytetrack_tracker import Tracker
from scripts.temp_speed_tracking import SpeedDetection


class SpeedCam :
    VIDEO_FILE = "vid_files/vehicle-counting1.mp4"
    
    def __init__(self) :
        pass

    
    def display_vid_n_predict(self, invid=VIDEO_FILE, speed_engine=False) :
        """Groups all the elements of the speed detection engine together and
        performs detection on the provided video stream

        Args:
            invid (str, optional): Video file to play. Defaults to VIDEO_FILE.
            speed_engine (bool, optional): Whether to run the engine or just simple
                play the specified video.
        """
        cap = cv2.VideoCapture(invid)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"fps: {fps}")
        while cap.isOpened() :
            ret, frame = cap.read()
            if ret == False :
                print("Exiting video player")
                break
            
            if speed_engine :
                # Use yolov8 to perform vehicle detection
                detections = detector.object_detection_on_vid(frame)
                
                # Apply the vehicle tracker to the frame to id and track the vehicles
                detected_data = detections.boxes.data.tolist()
                tracker.update(frame, detected_data)
                
                # Create a hash map mapping the id of each vehicle to its reference point(here the centre of the detection box)
                vehicle_ref = dict()
                for detection in tracker.tracks :
                    centre_x = ((detection.rect[2] - detection.rect[0])/2) + detection.rect[0]
                    centre_y = ((detection.rect[3] - detection.rect[1])/2) + detection.rect[1]
                    vehicle_ref[detection.tracker_id] = (centre_x, centre_y)
                # Pass vehicle_ref into the speed estimator
                speed_estimator.process_coordinates(vehicle_ref)
                
                
                # Annotate and draw boxes around vehicles in the frame
                frame = detector.annotate_vehicles(frame, tracker.tracks, speed_estimator.vehicle_speeds)
                
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()
        

detector = Detection()
tracker = Tracker()
speed_estimator = SpeedDetection()

if __name__ == "__main__" :
    ai_cam = SpeedCam()
    ai_cam.display_vid_n_predict(speed_engine=True)