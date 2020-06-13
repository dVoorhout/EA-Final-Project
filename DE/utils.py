import matplotlib.pyplot as plt
from math import sqrt
from time import sleep, time

def get_coordinates(solution):
    # Decodes the solution into x and y coordinates
    # The solution are encoded as an array of [x1, y1, x2, y2, ..., xn, yn]
    x = []
    y = []
    for i in range(0, len(solution), 2):
        x.append(solution[i])
        y.append(solution[i+1])
    return x, y


def plot_solution(solution):
    x, y = get_coordinates(solution)
    plt.plot(x, y, '.')
    plt.show()

def plot_best_solution_progress(solutions, duration=20):
    # Animation on how the best solution progresses
    fig, ax = plt.subplots(figsize=(10, 10))
    h1, = ax.plot([], [], '.')
    
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    
    for i, solution in enumerate(solutions):
        x, y = get_coordinates(solution)
        
        h1.set_data(x, y)
        ax.set_title(f"Generation {i+1}")
        fig.canvas.draw()

        sleep(duration/len(solutions))
        
def plot_population_progress(populations, best_solutions, duration=20):
    # Animation on how the population progresses
    fig, ax = plt.subplots(figsize=(8, 8))
    
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    
    ax.set_xlim([-0.1, 1.1])
    ax.set_ylim([-0.1, 1.1])
    
    fig_points = [ax.plot([], [], 'b.')[0] for i in range(len(populations[0]))]
    fig_points.append(ax.plot([], [], 'r.')[0]) # Additial for the best solution

    for i, (population, best_solution) in enumerate(zip(populations, best_solutions)):
        start_time = time()
        # Plot the solutions in a generation
        for j, solution in enumerate(population):
            x, y = get_coordinates(solution)
            fig_points[j].set_data(x, y)
        
        # Plot best solution
        x, y = get_coordinates(best_solution)
        fig_points[j+1].set_data(x, y)
        
        ax.set_title(f"Generation {i+1}")
        fig.canvas.draw()
        
        end_time = time()
        
        # Note: there a lower bound on the duration of the animation based speed of the computer and the size of the population
        sleep(max(0, duration/len(populations) - (end_time-start_time)))
    

def plot_obj_value_progress(obj_values, optimum, title=None):
    x = range(1, len(obj_values)+1)
    plt.plot(x, obj_values)
    plt.hlines(optimum, x[0], x[-1])
    
#     plt.ylim([0, optimum*1.1])
    plt.xlabel("Generation")
    plt.ylabel("Objective value")
    plt.title(title)


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
    for i in range(0, len(solution), 2):
        for j in range(0, len(solution), 2):
            if i != j:
                x1, y1 = solution[i:i+2]
                x2, y2 = solution[j:j+2]
                result = sqrt((x1 - x2)**2 + (y1 - y2)**2)
                if result < d:
                    d = result
    return d

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


def find_reliable(algo, max_evaluations=None, max_generations=None, min_pop_diff=10**-10,):
    # Returns True when the algorithm can find the optimum 10 times a row otherwise False
    for i in range(1, 11):
        print(f"RUN #{i}")
        algo.reset()
        algo.run(max_evaluations=max_evaluations,
                 max_generations=max_generations,
                 stop_on_small_pop_diff=min_pop_diff, # Stop when the diff between avg_obj_val and best_obj_val is too small 
                 verbose=False) # Willl crash the jupyter notebook when turned on with many experiments

        print("\tAVG_OBJ: ", algo.iter_avg_obj_val[-1])
        print("\tBEST_OBJ:", algo.iter_best_obj_val[-1])
        print("\tEVALUATIONS:", algo.evaluations)
        if not algo.found_optimum:
            return False
    return True