from dataclasses import dataclass
import numpy as np


LINE1_LEFT = (335, 408)
LINE1_RIGHT = (1087, 408)
LINE2_LEFT = (212, 498)
LINE2_RIGHT = (1275, 498)

PHYSICAL_DIST = 12 #meters
FPS = 25.0


@dataclass
class DetectionObj :
    rect: list
    class_id: int
    confidence: float
    tracker_id: int = None

    @classmethod
    def from_results(cls, pred) :
        result = []
        for top_l_x, top_l_y, btm_r_x, btm_r_y, confidence, class_id in pred:
            class_id = int(class_id)
            result.append(DetectionObj(
                rect = [int(top_l_x),
                      int(top_l_y),
                      int(btm_r_x),
                      int(btm_r_y)],
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
        

# Not in use
@dataclass
class SpeedObj :
    vehicle_centre: tuple
    vehicle_id: int


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