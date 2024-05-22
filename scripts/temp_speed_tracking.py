from collections import defaultdict

from scripts.helpers import LINE1_LEFT, LINE1_RIGHT, LINE2_LEFT, LINE2_RIGHT
from scripts.helpers import PHYSICAL_DIST, FPS, SPEED_LIMIT


class SpeedDetection :
    
    def __init__(self) :
        self.vehicles_tracked = dict()
        self.LINE1_M, self.LINE1_C = self.line_slope_n_intercept(LINE1_LEFT, LINE1_RIGHT)
        self.LINE2_M, self.LINE2_C = self.line_slope_n_intercept(LINE2_LEFT, LINE2_RIGHT)
        self.vehicle_speeds = defaultdict(lambda: None)
        self.violators = defaultdict(lambda: None)
        self.past_violators = list()
    
    
    def process_coordinates(self, vehicle_ref) :
        for vehicle_id in vehicle_ref :
            cent_x, cent_y = vehicle_ref[vehicle_id]
            if vehicle_id not in self.vehicles_tracked and (self.LINE2_M * cent_x + self.LINE2_C - cent_y) <= 0 :
                print("Continuing here!")
                continue
            elif vehicle_id not in self.vehicles_tracked :
                eqn = self.LINE1_M * cent_x + self.LINE1_C - cent_y
                if eqn <= 0 :
                    print("YES.. added to tracked")
                    self.vehicles_tracked[vehicle_id] = 1
            else :
                self.vehicles_tracked[vehicle_id] += 1
                eqn = self.LINE2_M * cent_x + self.LINE2_C - cent_y
                if (eqn) <= 0 :
                    print("YES.. in tracked and crossed second line")
                    speed = self.speed_estimator(self.vehicles_tracked[vehicle_id])
                    self.vehicle_speeds[vehicle_id] = speed
                    # Check if speed is being violated
                    if speed > SPEED_LIMIT and vehicle_id not in self.violators :
                        self.violators[vehicle_id] = speed
                        self.past_violators.append(vehicle_id)
                    # Add speed to the dict
                    del self.vehicles_tracked[vehicle_id]
        print(f"self.vehicles_tracked: {self.vehicles_tracked}")


    def speed_estimator(self, no_frames) :
        seconds = no_frames/FPS
        return (PHYSICAL_DIST/seconds) * (18/5) #km/h
            
            
    def line_slope_n_intercept(self, p1, p2) :
        x1, y1 = p1
        x2, y2 = p2
        m = (y2 - y1)/(x2 - x1)
        c = y1 - (x1 * (y2 - y1)/(x2 - x1))
        
        return m, c
            
            
speed_estimator = SpeedDetection()