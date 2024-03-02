import cv2
from ultralytics import YOLO


class SpeedCam :
    MODEL = "yolov8l.pt"
    VIDEO_FILE = "vehicle-counting1.mp4"

    def __init__(self) :
        print("Loading model...")
        self.model = YOLO(self.MODEL)
        print("Done Loading! Now Fusing Model...")
        self.model.fuse()
        print("Done with the fuse!")
    

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
                detections = self.object_detection_on_vid(frame)
            
            cv2.imshow("Frame", frame)
            if cv2.waitKey(25) & 0xFF==ord("q") :
                break

        cap.release()
        cv2.destroyAllWindows()
        
        
    def object_detection_on_vid(self, frame) :
            detections = self.model(frame)[0]
            print(f"detections.boxes: {detections.boxes}")
            return detections
        
    
    def annotate_vehicles(self, boxes) :
        pass


if __name__ == "__main__" :

    object_detection_on_vid()