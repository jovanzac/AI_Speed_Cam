import os
import numpy as np
from dataclasses import dataclass
from cryptography.fernet import Fernet


LINE1_LEFT = (335, 408)
LINE1_RIGHT = (1087, 408)
LINE2_LEFT = (212, 498)
LINE2_RIGHT = (1275, 498)

# LINE1_LEFT = (274, 315)
# LINE1_RIGHT = (782, 305)
# LINE2_LEFT = (300, 359)
# LINE2_RIGHT = (855, 347)

PHYSICAL_DIST = 12 #meters
FPS = 25.0
SPEED_LIMIT = 20 #km/hr


KEY = os.environ.get("PASSWORD_KEY")
crypter = Fernet(KEY)


@dataclass
class DetectionObj :
    vehicle_rect: list
    class_id: int
    confidence: float
    plate_rect: list = None
    tracker_id: int = None
    violation: bool = False

    @classmethod
    def from_results(cls, pred) :
        result = []
        for top_l_x, top_l_y, btm_r_x, btm_r_y, confidence, class_id in pred:
            class_id = int(class_id)
            result.append(DetectionObj(
                vehicle_rect = [int(top_l_x),
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
            detection.vehicle_rect[0], 
            detection.vehicle_rect[1],
            detection.vehicle_rect[2],
            detection.vehicle_rect[3],
            detection.confidence
        ] if with_confidence else [
            detection.vehicle_rect[0], 
            detection.vehicle_rect[1],
            detection.vehicle_rect[2],
            detection.vehicle_rect[3]
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
    

    
    
def decode_psswd(encrypted_psswd) :
    decrypted_psswd = crypter.decrypt(encrypted_psswd)
    
    return str(decrypted_psswd, 'utf8')


def encode_psswd(raw_psswd) :
    encrypted_psswd = crypter.encrypt(raw_psswd.encode())
    
    return encrypted_psswd