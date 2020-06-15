import numpy as np

from Packomania import Packomania
from DE import DifferentialEvolution
from utils import *

from time import time
from random import seed


num_points_list = [2, 4, 5, 6, 7, 9]


def results2np(results_A3, results_A6):
    return np.array([results_A3['evaluations'], results_A6['evaluations']])


def benchmark(differential_weight, 
              crossover_prob,
              max_evaluations,
              optimum_accuracy,
              rng_seed=0):
    global num_points_list

    def _run(algo,
                max_evaluations=None,
                max_generations=None,
                min_pop_diff=10**-12,
                num_runs=10,
                verbose=True):
        results = dict()
        results['evaluations'] = []
        results['avg_obj_vals'] = []
        results['best_obj_vals'] = []
        results['exitflag'] = []
        results['optimum'] = 0

        avg_obj_val = 0
        best_obj_val = 0
        evaluations = 0

        max_eval_variable = max_evaluations

        for i in range(1, num_runs+1):
            print(f"RUN #{i}")
            evaluations = 0
            start_time = time()

            running = True
            while running:
                algo.reset()
                algo.run(max_evaluations=max_eval_variable,
                        max_generations=max_generations,
                        # Stop when the diff between avg_obj_val and best_obj_val is too small
                        stop_on_small_pop_diff=min_pop_diff,
                        verbose=False)  # Will crash the jupyter notebook when turned on with many experiments

                evaluations += algo.evaluations
                if algo.exitflag == Exitflag.pop_converged:
                    max_eval_variable = max_evaluations - evaluations
                else:
                    if verbose:
                        print("\tAVG_OBJ: ", algo.iter_avg_obj_val[-1])
                        print("\tBEST_OBJ:", algo.iter_best_obj_val[-1])
                        print("\tEVALUATIONS:", algo.evaluations)
                    print(f"\tRUN DURATION: {time()-start_time}s")

                    results['avg_obj_vals'].append(algo.iter_avg_obj_val[-1])
                    results['best_obj_vals'].append(algo.iter_best_obj_val[-1])
                    results['evaluations'].append(algo.evaluations)
                    results['exitflag'].append(algo.exitflag)

                    if algo.found_optimum:
                        results['optimum'] += 1
                    running = False



    seed(rng_seed)

    results = []
    for num_points in num_points_list:
        print("Num points: {}".format(num_points))
        dim = num_points*2

        popsize = 10*dim
        bounds = [[0, 1] for i in range(num_points*2)]
        pk = Packomania(num_points)
        optimum = pk.distance

        de = DifferentialEvolution(
            scattering_points,
            bounds,
            popsize,
            differential_weight,
            crossover_prob
        )
        de.set_optimum(optimum, optimum_accuracy)
        r = _run(algo=de,
                    stop_on_fail=False,
                    max_evaluations=max_evaluations)
        results.append(r)

    return results


# Accuracy 1e-3
results_A3 = benchmark(differential_weight=0.5,
                       crossover_prob=0.3,
                       max_evaluations=5e6,
                       optimum_accuracy=1e-3)

save_reliable_results('Benchmark/BB_A3.csv', num_points_list, results_A3, x_name='num_points')
save_pickle('Benchmark/DE_BB_A3.pickle', results_A3)


# Accuracy 1e-6
results_A6 = benchmark(differential_weight=0.5,
                       crossover_prob=0.3,
                       max_evaluations=5e6,
                       optimum_accuracy=1e-6)

save_reliable_results('Benchmark/BB_A6.csv', num_points_list, results_A3, x_name='num_points')
save_pickle('Benchmark/DE_BB_A6.pickle', results_A6)

# To numpy 
np_results = results2np(results_A3, results_A6)
np.save('Benchmark/DE_BB.pickle', np_results)