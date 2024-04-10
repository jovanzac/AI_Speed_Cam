from collections import defaultdict

from scripts.helpers import LINE1_LEFT, LINE1_RIGHT, LINE2_LEFT, LINE2_RIGHT
from scripts.helpers import PHYSICAL_DIST, FPS


class SpeedDetection :
    
    def __init__(self) :
        self.vehicles_tracked = dict()
        self.LINE1_M, self.LINE1_C = self.line_slope_n_intercept(LINE1_LEFT, LINE1_RIGHT)
        self.LINE2_M, self.LINE2_C = self.line_slope_n_intercept(LINE2_LEFT, LINE2_RIGHT)
        self.vehicle_speeds = defaultdict(lambda: None)
    
    
    def process_coordinates(self, vehicle_ref) :
        for vehicle_id in vehicle_ref :
            # print(f"vehicle_id: {vehicle_id}")
            cent_x, cent_y = vehicle_ref[vehicle_id]
            # print(f"cent_x, cent_y: {cent_x}, {cent_y}")
            if vehicle_id not in self.vehicles_tracked and (self.LINE2_M * cent_x + self.LINE2_C - cent_y) <= 0 :
                print("Continuing here!")
                continue
            elif vehicle_id not in self.vehicles_tracked :
                eqn = self.LINE1_M * cent_x + self.LINE1_C - cent_y
                # print(f"self.LINE1_C: {self.LINE1_C}     cent_y: {cent_y}")
                # print(f"1st line eqn for id{vehicle_id} : {eqn}")
                if eqn <= 0 :
                    print("YES.. added to tracked")
                    self.vehicles_tracked[vehicle_id] = 1
            else :
                self.vehicles_tracked[vehicle_id] += 1
                eqn = self.LINE2_M * cent_x + self.LINE2_C - cent_y
                # print(f"2nd line eqn: {eqn}")
                if (eqn) <= 0 :
                    print("YES.. in tracked and crossed second line")
                    speed = self.speed_estimator(self.vehicles_tracked[vehicle_id])
                    self.vehicle_speeds[vehicle_id] = speed
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
            