import cv2
from ultralytics import YOLO


class SpeedCam :
    MODEL = "yolov8l.pt"
    VIDEO_FILE = "vid_files/vehicle-counting1.mp4"

    def __init__(self) :
        print("Loading model...")
        self.model = YOLO(self.MODEL)
        print("Done Loading! Now Fusing Model...")
        self.model.fuse()
        print("Done with the fuse!")
        
        self.object_classes = self.model.model.names
    

    def resize_n_write_video(self, out_vid, in_vid=VIDEO_FILE) :
        """Can be used to resize the frames of a specified video and
        write the new frames out to a new location.

        Args:
            out_vid (str): filename for the new video file. Must have the extension .mp4
            in_vid (str, optional): Defaults to VIDEO_FILE. Specified the video file to resize
        """
        output = cv2.VideoWriter(out_vid, cv2.VideoWriter_fourcc(*'mp4v'), 25, (1459, 821))
        cap = cv2.VideoCapture(in_vid)
        while cap.isOpened() :
            ret, frame = cap.read()
            if ret == False :
                print("Exiting video player")
                break
            
            # Resize the frame
            print(type(frame.shape[0]))
            print(f"frame width: {frame.shape[0]}   height: {frame.shape[1]}")
            resized_frame = cv2.resize(frame, (0,0), fx=0.38, fy=0.38)
            print(f"new frame width: {resized_frame.shape[0]}   height: {resized_frame.shape[1]}")
            
            # writing the new frame in output 
            output.write(resized_frame)
            cv2.imshow("Frame", resized_frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()


    def display_vid_n_predict(self, invid=VIDEO_FILE, speed_engine=False) :
        """Simply plays a video file

        Args:
            invid (str, optional): Video file to play. Defaults to VIDEO_FILE.
        """
        cap = cv2.VideoCapture(invid)
        while cap.isOpened() :
            ret, frame = cap.read()
            if ret == False :
                print("Exiting video player")
                break
            
            if speed_engine :
                # Use yolov8 to perform vehicle detection
                detections = self.object_detection_on_vid(frame)
                # Annotate and draw boxes around vehicles in the frame
                frame = self.annotate_vehicles(frame, detections.boxes)
                
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()
        
        
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
    
    
    def annotate_vehicles(self, frame, boxes) :
        # Initializing the font configurations
        FONT = cv2.FONT_HERSHEY_COMPLEX_SMALL
        FONTSCALE = 1
        THICKNESS = 2
        
        # xy locations and classes of all vehicles
        xyxy = boxes.xyxy.tolist()
        classes = boxes.cls.tolist()
        for vehicle, vehicle_class in zip(xyxy, classes) :
            vehicle = [int(i) for i in vehicle]
            # color correspondign to the vehicle
            color = self.bounding_box_color(vehicle_class)
            print(f"vehicle[:2]: {vehicle[:2]}")
            print(f"vehicle[2:]: {vehicle[2:]}")
            frame = cv2.rectangle(frame, vehicle[:2], vehicle[2:], color, 2)
            frame = cv2.putText(frame, f'{self.object_classes[vehicle_class]}', (vehicle[0], vehicle[1]-5), FONT,  
                   FONTSCALE, color, THICKNESS, cv2.LINE_AA)
        
        return frame


if __name__ == "__main__" :
    system = SpeedCam()
    system.display_vid_n_predict(speed_engine=True)