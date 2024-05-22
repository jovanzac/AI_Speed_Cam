import cv2


class SupportTools :
    VIDEO_FILE = "vid_files/test2.mp4"
    
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
        
        
if __name__ == "__main__" :
    tools = SupportTools()
    tools.resize_n_write_video("test2_resized.mp4")