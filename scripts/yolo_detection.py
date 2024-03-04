import cv2
from ultralytics import YOLO


class Detection :
    MODEL = "models/yolov8l.pt"
    VIDEO_FILE = "vid_files/vehicle-counting1.mp4"

    def __init__(self) :
        print("Loading model...")
        self.model = YOLO(self.MODEL)
        print("Done Loading! Now Fusing Model...")
        self.model.fuse()
        print("Done with the fuse!")
        
        self.object_classes = self.model.model.names
        
        
    def object_detection_on_vid(self, frame) :
            detections = self.model(frame)[0]
            return detections
        
    
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
                frame = self.annotate_vehicles(frame, detected_data)
                
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()
    
    
    def annotate_vehicles(self, frame, detections, tracked_ids=None) :
        # Initializing the font configurations
        FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
        FONTSCALE = 1
        THICKNESS = 2
        
        if tracked_ids :
            for vehicle, id in zip(detections, tracked_ids) :
                bbox = [int(i) for i in vehicle[:4]]
                # color correspondign to the vehicle
                color = self.bounding_box_color(vehicle[5])
                frame = cv2.rectangle(frame, bbox[:2], bbox[2:], color, 2)
                frame = cv2.putText(frame, f'#{id}. {self.object_classes[vehicle[5]]}', (bbox[0], bbox[1]-5), FONT,  
                    FONTSCALE, color, THICKNESS, cv2.LINE_AA)
        else :
            for vehicle in detections :
                bbox = [int(i) for i in vehicle[:4]]
                # color correspondign to the vehicle
                color = self.bounding_box_color(vehicle[5])
                frame = cv2.rectangle(frame, bbox[:2], bbox[2:], color, 2)
                frame = cv2.putText(frame, f'{self.object_classes[vehicle[5]]}', (bbox[0], bbox[1]-5), FONT,  
                    FONTSCALE, color, THICKNESS, cv2.LINE_AA)
        
        return frame


if __name__ == "__main__" :
    system = Detection()
    system.display_vid_n_predict(detection_engine=True)
    # system.display_vid_n_predict()