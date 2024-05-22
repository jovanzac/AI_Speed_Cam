import numpy as np

from dataclasses import dataclass

from ByteTrack.yolox.tracker.byte_tracker import BYTETracker, STrack
from onemetric.cv.utils.iou import box_iou_batch

from scripts.helpers import DetectionObj, detections2boxes, tracks2boxes


@dataclass(frozen=True)
class BYTETrackerArgs:
    track_thresh: float = 0.25
    track_buffer: int = 30
    match_thresh: float = 0.8
    aspect_ratio_thresh: float = 3.0
    min_box_area: float = 1.0
    mot20: bool = False


class Tracker :
    def __init__(self) :
        # initiate tracker
        self.byte_tracker = BYTETracker(BYTETrackerArgs())
        self.tracks = None


    # matches our bounding boxes with predictions
    def match_detections_with_tracks(self, detections, tracks) :
        detection_boxes = detections2boxes(detections=detections, with_confidence=False)
        tracks_boxes = tracks2boxes(tracks=tracks)
        iou = box_iou_batch(tracks_boxes, detection_boxes)
        track2detection = np.argmax(iou, axis=1)
        
        for tracker_index, detection_index in enumerate(track2detection):
            if iou[tracker_index, detection_index] != 0:
                detections[detection_index].tracker_id = tracks[tracker_index].track_id
        for detection in detections :
            if detection.tracker_id == None :
                detections.remove(detection)
            
        return detections


    def update(self, frame, detections) :
        # Convert the detections to <class> Detection type
        detections = DetectionObj.from_results(pred=detections)
        # track players
        tracks = self.byte_tracker.update(
            output_results = detections2boxes(detections=detections),
            img_info = frame.shape,
            img_size = frame.shape
        )

        tracked_detections = self.match_detections_with_tracks(detections=detections, tracks=tracks)
        self.tracks = tracked_detections
        

tracker = Tracker()