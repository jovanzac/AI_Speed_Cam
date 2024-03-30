import cv2
from scripts.yolo_detection import Detection
from scripts.deepsort_tracker import Tracker


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
                tracked_ids = list()
                for track in tracker.tracks :
                    track_id = track.track_id
                    tracked_ids.append(track_id)
                
                # Annotate and draw boxes around vehicles in the frame
                frame = detector.annotate_vehicles(frame, detected_data, tracked_ids)
                
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()
        

detector = Detection()
tracker = Tracker()

if __name__ == "__main__" :
    ai_cam = SpeedCam()
    ai_cam.display_vid_n_predict(speed_engine=True)