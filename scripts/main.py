import cv2
import dotenv


class SpeedCam :
    # VIDEO_FILE = "vid_files/vehicle-counting1.mp4"
    VIDEO_FILE = "vid_files/test2_resized.mp4"
    
    def __init__(self, detector, tracker, speed_estimator, db_manager) :
        self.detector = detector
        self.tracker = tracker
        self.speed_estimator = speed_estimator
        self.db_manager = db_manager


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
                detections = self.detector.object_detection_on_vid(frame)
                
                # Apply the vehicle self.tracker to the frame to id and track the vehicles
                detected_data = detections.boxes.data.tolist()
                self.tracker.update(frame, detected_data)
                
                # Create a hash map mapping the id of each vehicle to its reference point(here the centre of the detection box)
                vehicle_ref = dict()
                for detection in self.tracker.tracks :
                    centre_x = ((detection.vehicle_rect[2] - detection.vehicle_rect[0])/2) + detection.vehicle_rect[0]
                    centre_y = ((detection.vehicle_rect[3] - detection.vehicle_rect[1])/2) + detection.vehicle_rect[1]
                    vehicle_ref[detection.tracker_id] = (centre_x, centre_y)
                # Pass vehicle_ref into the speed estimator
                self.speed_estimator.process_coordinates(vehicle_ref)
                # If any vehicle is violating the speed limit, detect its number plate
                if self.speed_estimator.violators :
                    # Detect number plate's bounding box
                    plates = self.detector.plate_detection_for_vehicle(frame, self.tracker.tracks, self.speed_estimator.violators)
                    print(f"plates are: {plates}")
                    # Enhance the plate and detect the characters in it
                    for v_id in plates :
                        if self.detector.plate_counter[v_id] >= 3 :
                            continue
                        # Create an image of the plate and add it to local storage
                        file_loc = self.detector.extract_plate_from_img(frame, plates[v_id], v_id)
                        # Put the image of the plate into firebase storage.
                        self.db_manager.plates_to_storage(file_loc=file_loc)

                # Annotate and draw boxes around vehicles in the frame
                frame = self.detector.annotate_vehicles(frame, self.tracker.tracks, self.speed_estimator.vehicle_speeds, True, self.speed_estimator.violators)
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__" :
    # Load the environment variables
    dotenv.load_dotenv(override=True)
    
    from scripts.yolo_detection import detector
    from scripts.bytetrack_tracker import tracker
    from scripts.temp_speed_tracking import speed_estimator
    from scripts.db_manager import db_manager
    
    ai_cam = SpeedCam(detector, tracker, speed_estimator, db_manager)
    ai_cam.display_vid_n_predict(speed_engine=True)