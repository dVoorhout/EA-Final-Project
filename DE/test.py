from random import randint, random
from utils import get_stricter_bounds

class DE:
    def __init__(self, agent_length, crossover_prob):
        self.crossover_prob = crossover_prob
        self.agent_length = agent_length
        self.population_bottleneck_points = [(1,2,3,4), (1,2,3,4)]
    
    
    def crossover_on_points(self, target_idx, target, mutated):
        # Crossover on points 
        n = randint(0, (self.agent_length-2) / 2)*2
        
        L = 2
        while random() < self.crossover_prob and L < self.agent_length - n:
            L += 2
        
        new_agent = target[:n] + mutated[n:n+L] + target[n+L:]
        return new_agent


    def crossover_best_points2(self, target_idx, target, mutated):
        n = randint(0,1)

        bottleneck_points = self.population_bottleneck_points[target_idx]

        starting_point = bottleneck_points[n*2] # times 2 since for (x1,y1,x2,y2) it will selected either x1 or y1

        L = 2 # 2 to select both the x and y coordinates

        while random() < self.crossover_prob and L < self.agent_length - n:
            L += 2
        
        new_agent = target[:n] + mutated[n:n+L] + target[n+L:]
        return new_agent


# target = [5,6,7,8]
# mutated = [-1,-2,-3,-4]
# d = DE(len(target), crossover_prob=0.5)

# new_agent = d.crossover_on_points(0, target, mutated)
# print(new_agent)

print(get_stricter_bounds(7))