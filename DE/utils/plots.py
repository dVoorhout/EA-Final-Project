import matplotlib.pyplot as plt

from time import time, sleep

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
    fig_points.append(ax.plot([], [], 'r.')[0]) # Additional for the best solution

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