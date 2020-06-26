from math import sqrt

def scattering_points_slower(solution):
    # Scattering points problem
    # The solution are encoded as an array of [x1, y1, x2, y2, ..., xn, yn]
    
    d = []
    for i in range(0, len(solution), 2):
        for j in range(0, len(solution), 2):
            if i != j:
                x1, y1 = solution[i:i+2]
                x2, y2 = solution[j:j+2]
                d.append(sqrt((x1 - x2)**2 + (y1 - y2)**2))
    return min(d)


def scattering_points(solution):
    # Scattering points problem
    # The solution are encoded as an array of [x1, y1, x2, y2, ..., xn, yn]
    
    d = 10 # The distance between 2 points inside a unit square cannot be larger than 10
    bottleneck_points = () # The points that determine the objective value
    for i in range(0, len(solution), 2):
        for j in range(0, len(solution), 2):
            if i != j:
                x1, y1 = solution[i:i+2]
                x2, y2 = solution[j:j+2]
                result = (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)
                if result < d:
                    d = result
                    bottleneck_points = (i, i+1, j, j+1)
    return sqrt(d), bottleneck_points


def get_stricter_bounds(num_points):
    # Split the bounds of [0,1] into smaller bounds for each points such that each point is in its own compartment
    bounds = []
    squares = int(sqrt(num_points))
    
    dx = 1 / squares
    dy = 1 / squares
    
    for y in range(squares):
        y_lb = y * dy
        y_ub = (y+1) * dy
        for x in range(squares):
            x_lb = x * dx
            x_ub = (x+1) * dx
            bounds.append([x_lb, x_ub])
            bounds.append([y_lb, y_ub])
    
    # Add the remaining bounds to be [0,1]
    for i in range(num_points*2 - len(bounds)):
        bounds.append([0, 1])
    return bounds