import cv2
from ultralytics import YOLO
from onemetric.cv.utils.iou import box_iou_batch
from collections import defaultdict

from scripts.helpers import DetectionObj
from scripts.helpers import LINE1_LEFT, LINE1_RIGHT, LINE2_LEFT, LINE2_RIGHT


class Detection :
    MODEL = "models/yolov8l.pt"
    PLATE_MODEL = "models/license_plate_detector.pt"
    VIDEO_FILE = "vid_files/vehicle-counting1.mp4"

    def __init__(self) :
        print("Loading vehicle detection YOLO model...")
        self.model = YOLO(self.MODEL)
        print("Done Loading! Now Fusing Model...")
        print("Loading plate detection YOLO model...")
        self.plate_model = YOLO(self.PLATE_MODEL)
        print("Done Loading! Now Fusing Model...")
        self.plate_model.fuse()
        print("Done with the fuse!")
        
        self.object_classes = self.model.model.names
        self.plate_counter = defaultdict(lambda: 0)
        
        
    def object_detection_on_vid(self, frame) :
            detections = self.model.predict(frame, conf=0.3, classes=[1, 2, 3, 5, 7])[0]
            return detections
        
        
    def plate_detection_on_vid(self, frame) :
        detections = self.plate_model.predict(frame, conf=0.3)[0]
        return detections
    
    def plate_detection_for_vehicle(self, frame, vehicles, violators) :
        """Finds the correct bounding boxes of number plates corresponding to cars
        that have violated the speed limit.

        Args:
            frame (np.array): A numpy array representing the video frame
            vehicles (<class> DetectionObj): An object representing and holding all the attibutes of vehicles. 
            violators (dict): A dict of all the vehicles violating the speed limit
        """
        violating_plates = dict()
        all_plates = self.plate_detection_on_vid(frame).boxes.data.tolist()
        for vehicle in vehicles :
            if vehicle.tracker_id in violators :
                cx1, cy1, cx2, cy2 = vehicle.vehicle_rect
                for px1, py1, px2, py2, _, _ in all_plates :
                    if (cx1<px1 and cy1<py1) and (cx2>px2 and cy2>py2) :
                        vehicle.plate_rect = [
                            int(px1), int(py1), int(px2), int(py2)
                        ]
                        violating_plates[vehicle.tracker_id] = vehicle.plate_rect

        return violating_plates
        
    
    def bounding_box_color(self, label) :
        if label == 0 : # Person
            color = (255, 85, 45) # purple
        elif label == 1 : # Bicycle
            color = (51, 34, 164) # forrest green
        elif label == 2 : # Car
            color = (175, 222, 82) # pink
        elif label == 3 :  # Motobike
            color = (255, 0, 204) # teal
        elif label == 5 :  # Bus
            color = (255, 0, 149) # darker teal
        elif label == 7 : # Truck
            color = (71, 246, 227) # gold
        else:
            color = (255, 0, 0)
        return color
    
    
    def extract_plate_from_img(self, frame, plate, vehicle_id) :
        """Create a new image of the plate alone

        Args:
            frame : the complete image frame
            plate (list): the bounding box of the number plate
            vehicle_id (int): the id of the vehicle the plate belongs to
        """
        if vehicle_id in self.plate_counter :
            self.plate_counter[vehicle_id] += 1
        else :
            self.plate_counter[vehicle_id] = 1
        IMG_NAME = f"plate{vehicle_id}-{self.plate_counter[vehicle_id]}"
        PLATES_DIR = "./plates/"
        plate_img = frame[plate[1]:plate[3], plate[0]:plate[2]]
        plate_loc = f"{PLATES_DIR}{IMG_NAME}.png"
        cv2.imwrite(plate_loc, plate_img)
        
        return plate_loc
    
    
    def display_vid_n_predict(self, invid=VIDEO_FILE, detection_engine=False) :
        """Used for simply detecing vehicles in each frame of the video.

        Args:
            invid (str, optional): Video file to play. Defaults to VIDEO_FILE.
            detection_engine (bool, optional): if speed_engine is not specified or is set to
                False, the video clip is simply played. Otherwise vehicles in each frame
                are detected and displayed.
        """
        cap = cv2.VideoCapture(invid)
        while cap.isOpened() :
            ret, frame = cap.read()
            if ret == False :
                print("Exiting video player")
                break
            
            if detection_engine :
                # Use yolov8 to perform vehicle detection
                detections = self.object_detection_on_vid(frame)
                # Annotate and draw boxes around vehicles in the frame
                detected_data = detections.boxes.data.tolist()
                tracks = [DetectionObj(pred=detection) for detection in detected_data]
                frame = self.annotate_vehicles(frame, tracks, tracking=False)
                
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()
    
    
    def annotate_vehicles(self, frame, tracks, vehicle_speeds=None, tracking=True, violators=[]) :
        # Initializing the font configurations
        FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
        FONTSCALE = 1
        THICKNESS = 2
        
        if tracking and vehicle_speeds != None :
            for detection in tracks :
                det_id = detection.tracker_id
                bbox = detection.vehicle_rect
                # color corresponding to the vehicle
                color = self.bounding_box_color(detection.class_id) if det_id not in violators else (0, 0, 255)
                frame = cv2.rectangle(frame, bbox[:2], bbox[2:], color, 2)
                # frame = cv2.putText(frame, f'#{detection.tracker_id}. {self.object_classes[detection.class_id]}', (bbox[0], bbox[1]-5), FONT,  
                #     FONTSCALE, color, THICKNESS, cv2.LINE_AA)
                speed = f"{round(vehicle_speeds[det_id])} km/h" if vehicle_speeds[det_id] != None else None
                frame = cv2.putText(frame, f'#{det_id}. speed:{speed}', (bbox[0], bbox[1]-5), FONT,
                    FONTSCALE, color, 1, cv2.LINE_AA)
        else :
            for detection in tracks :
                bbox = detection.vehicle_rect
                # color corresponding to the vehicle
                color = self.bounding_box_color(detection.class_id)
                frame = cv2.rectangle(frame, bbox[:2], bbox[2:], color, 2)
                frame = cv2.putText(frame, f'{self.object_classes[detection.class_id]}', (bbox[0], bbox[1]-5), FONT,  
                    FONTSCALE, color, THICKNESS, cv2.LINE_AA)
        
        frame = cv2.line(frame, LINE1_LEFT, LINE1_RIGHT, (51, 34, 164), THICKNESS)
        frame = cv2.line(frame, LINE2_LEFT, LINE2_RIGHT, (51, 34, 164), THICKNESS)
        
        return frame


# detector = Detection()


if __name__ == "__main__" :
    # system = Detection()
    # system.display_vid_n_predict(detection_engine=True)
    print("Code cannot be executed from this scope. Go to root directory of the project and write a script to execute it there")
