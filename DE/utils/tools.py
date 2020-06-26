import numpy as np
import pickle

from time import time

class Exitflag:
    optimum = 1
    max_evals = -1
    max_gen = -2
    pop_converged = -3
    no_improvements = -4
    no_improvements_gen_10 = -5


def find_reliable(algo, 
                  stop_on_fail=True,
                  max_evaluations=None, 
                  max_generations=None, 
                  min_pop_diff=10**-12, 
                  num_runs=10,
                  crossover='std',
                  verbose=True):
    # Returns True when the algorithm can find the optimum 10 times a row otherwise False
    results = dict()
    results['evaluations'] = []
    results['avg_obj_vals'] = []
    results['best_obj_vals'] = []
    results['exitflag'] = []
    results['optimum'] = 0
    
    failed_flag = False
    for i in range(1, num_runs+1):
        print(f"RUN #{i}")
        start_time = time()
        algo.reset()
        algo.run(
            crossover=crossover,
            max_evaluations=max_evaluations,
            max_generations=max_generations,
            stop_on_small_pop_diff=min_pop_diff, # Stop when the diff between avg_obj_val and best_obj_val is too small 
            verbose=False) # Will crash the jupyter notebook when turned on with many experiments

        if verbose:
            print("\tAVG_OBJ: ", algo.iter_avg_obj_val[-1])
            print("\tBEST_OBJ:", algo.iter_best_obj_val[-1])
            print("\tEVALUATIONS:", algo.evaluations)
        print(f"\tRUN DURATION: {time()-start_time}s")
        
        
        results['avg_obj_vals'].append(algo.iter_avg_obj_val[-1])
        results['best_obj_vals'].append(algo.iter_best_obj_val[-1])
        results['evaluations'].append(algo.evaluations)
        results['exitflag'].append(algo.exitflag)
        
        if not algo.found_optimum:
            failed_flag = True
        else:
            results['optimum'] += 1
        
        if stop_on_fail and failed_flag:
            return failed_flag, results
    return failed_flag, results


def eva_filter_fails(results):
    # Filters out the attempts where either the population converges or there was no improvements
    eva_filtered = []
    for i, exitflag in enumerate(results['exitflag']):
        if exitflag not in [Exitflag.pop_converged, Exitflag.no_improvements]:
            eva_filtered.append(results['evaluations'][i])
        else:
            print(f"Exitflag {exitflag}, Filtered {results['evaluations'][i]}")
    return eva_filtered



def save_reliable_results(filename, x, results, x_name="x"):
    with open(filename, 'w') as f:
        f.write(f"{x_name},VTR_reached_count,mean_evaluations,std_evaluations,mean_avg_obj_vals,std_avg_obj_vals,mean_best_obj_vals,std_best_obj_vals\n")
    
        for xx, r in zip(x, results):
            mean_eva = np.mean(eva_filter_fails(r))
            std_eva = np.std(eva_filter_fails(r))

            mean_avg_obj_vals = np.mean(r['avg_obj_vals'])
            std_avg_obj_vals = np.std(r['avg_obj_vals'])

            mean_best_obj_vals = np.mean(r['best_obj_vals'])
            std_best_obj_vals = np.std(r['best_obj_vals'])

            f.write(f"{xx},{r['optimum']},{mean_eva},{std_eva},{mean_avg_obj_vals},{std_avg_obj_vals},{mean_best_obj_vals},{std_best_obj_vals}\n")
            
            
def save_pickle(filename, obj):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)
        print("Saved object")

        
        
def load_pickle(filename):
    with open(filename, "rb") as f:
        results = pickle.load(f)
    return results
                         
        
    
