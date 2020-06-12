import matplotlib as plt
import numpy as np

PACKOMANIA_DIR = r"./Packomania/"


class Packomania():
    def __init__(self, num_points):
        self.num_points = num_points
        
        self.circle_origin = []
        self.circle_radius = 0
                
        self.read_radius()
        self.read_origin()

        self.points = [] # Does not work
        self.points_min_dist = -2*self.circle_radius / (2*self.circle_radius - 1)
        
        # self.convert_to_scattering_points()
        
    
    def read_radius(self):
        self.circle_radius = []
        with open(f"{PACKOMANIA_DIR}/radius.txt") as f:
            # File consits of: number of points, radius
            for line in f.read().split("\n")[:-1]: # Exclude last empty line
                num_circles, radius = line.split()
                
                if int(num_circles) == self.num_points:
                    self.circle_radius = float(radius)
                    break

    
    def read_origin(self):
        self.circle_origin = []
        with open(f"{PACKOMANIA_DIR}/csq_coords/csq{self.num_points}.txt", "r") as f:
            # File consists of: point idy
            for line in f.read().split("\n")[:-1]: # Exclude last empty line
                self.circle_origin.append(np.array(line.split()[1:], dtype=np.float64)) # Exclude point id
                
    
    def convert_to_scattering_points(self):
        # Doesn't work yet for points not on the border. 
        X, Y = (0, 1)
        
        # precision = 1e-15
        precision = 1e-10
        
        for point in self.circle_origin:
            # Convert coordinates system from [-0.5, 0.5] to [0, 1]
            print("Before", point)
            
            # point[X] = point[X]+0.5
            # point[Y] = point[Y]+0.5

            print("After ", point)
            print()
            
            # X axis
            if abs(point[X] - self.circle_radius - 0) < precision:
                self.points.append(0)
            elif abs(point[X] + self.circle_radius - 1) < precision:
                self.points.append(1)
            else:
                self.points.append(point[X])
                
            # Y axis
            if abs(point[Y] - self.circle_radius - 0) < precision:
                self.points.append(0)
            elif abs(point[Y] + self.circle_radius - 1) < precision:
                self.points.append(1)
            else:
                self.points.append(point[Y])
                