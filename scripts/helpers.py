from dataclasses import dataclass
import numpy as np


@dataclass
class DetectionObj :
    rect: list
    class_id: int
    confidence: float
    tracker_id: int = None

    @classmethod
    def from_results(cls, pred) :
        result = []
        for x_min, y_min, x_max, y_max, confidence, class_id in pred:
            class_id = int(class_id)
            result.append(DetectionObj(
                rect = [int(x_min),
                      int(y_min),
                      int(x_max),
                      int(y_max)],
                class_id = class_id,
                confidence = float(confidence)
            ))
        return result
    
    
    def class_attributes(self) :
        return [
            self.rect,
            self.class_id,
            self.confidence,
            self.tracker_id
        ]
        
    
class Track :
    track_id = None
    detection = None
    
    def __init__(self, t_id, detection) :
        self.track_id = t_id
        self.detection = detection


def detections2boxes(detections, with_confidence = True) :
    return np.array([
        [
            detection.rect[0], 
            detection.rect[1],
            detection.rect[2],
            detection.rect[3],
            detection.confidence
        ] if with_confidence else [
            detection.rect[0], 
            detection.rect[1],
            detection.rect[2],
            detection.rect[3]
        ]
        for detection
        in detections
    ], dtype=float)
    
    
# converts List[STrack] into format that can be consumed by match_detections_with_tracks function
def tracks2boxes(tracks) :
    return np.array([
        track.tlbr
        for track
        in tracks
    ], dtype=float) 