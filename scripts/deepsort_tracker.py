from deep_sort.deep_sort.tracker import Tracker as DeepSortTracker
from deep_sort.tools import generate_detections
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection

import numpy as np

from scripts.helpers import DetectionObj


class Tracker :
    tracker = None
    encoder = None
    tracks = None
    
    def __init__(self) :
        max_cosine_dist = 0.4
        nn_budget = None
        
        encoder_model_file = "models/mars-small128.pb"
        
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_dist, nn_budget)
        self.tracker = DeepSortTracker(metric)
        self.encoder = generate_detections.create_box_encoder(encoder_model_file, batch_size=1)


    def update(self, frame, detections) :
        # print("$"*50)
        print("In tracker func!!!")
        if len(detections) == 0 :
            self.tracker.predict()
            self.tracker.update([])
            self.update_tracks()
            return
        classless_detections = [[int(i[0]), int(i[1]), int(i[2]), int(i[3]), i[4]] for i in detections]
        bboxes = np.asarray([d[:-1] for d in classless_detections])
        bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2]
        scores = [d[-1] for d in classless_detections]
        
        features = self.encoder(frame, bboxes)
        
        dets = []
        for bbox_id, bbox in enumerate(bboxes) :
            dets.append(Detection(bbox, scores[bbox_id], features[bbox_id]))
            
        self.tracker.predict()
        self.tracker.update(dets)
        self.update_tracks(detections)


    def update_tracks(self, detections) :
        tracks = []
        detections  = DetectionObj.from_results(pred=detections)
        
        for track, detection in zip(self.tracker.tracks, detections) :
            if not track.is_confirmed() or track.time_since_update > 1 :
                continue
            # bbox = track.to_tlbr()
            detection.tracker_id = track.track_id
            
            tracks.append(detection)
            
        self.tracks = tracks