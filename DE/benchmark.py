import numpy as np

from Packomania import Packomania
from DE import DifferentialEvolution
from utils import *

from time import time
from random import seed

def results2np_avg(results_A3, results_A6):
    mean_evals_A3 = [np.mean(r['evaluations']) for r in results_A3]
    mean_evals_A6 = [np.mean(r['evaluations']) for r in results_A6]
    return np.array([mean_evals_A3, mean_evals_A6])


def results2np(results_A3, results_A6):
    mean_evals_A3 = [np.array(r['evaluations']) for r in results_A3]
    mean_evals_A6 = [np.array(r['evaluations']) for r in results_A6]
    return np.array([mean_evals_A3, mean_evals_A6])

def get_popsize(dim, m=10):
    return m*dim


def benchmark(differential_weight, 
              crossover_prob,
              max_evaluations,
              optimum_accuracy,
              get_popsize_func,
              min_pop_variance,
              crossover='std',
              get_init_bounds_func=lambda num_points: [[0, 1] for i in range(num_points*2)],
              num_points_list=[2, 4, 5, 6, 7, 9],
              rng_seed=0):

    def _run(algo,
                max_evaluations=None,
                max_generations=None,
                min_pop_variance=1e-4,
                num_runs=10,
                crossover='std',
                verbose=True):
        results = dict()
        results['evaluations'] = []
        results['avg_obj_vals'] = []
        results['best_obj_vals'] = []
        results['exitflag'] = []
        results['optimum'] = 0
        results['restart'] = 0

        # avg_obj_val = 0
        # best_obj_val = 0
        # evaluations = 0

        # max_eval_variable = max_evaluations

        for i in range(1, num_runs+1):
            print(f"RUN #{i}")
            max_eval_variable = max_evaluations
            evaluations = 0
            start_time = time()

            running = True
            while running:
                algo.reset()
                algo.run(max_evaluations=max_eval_variable,
                        max_generations=max_generations,
                        # Stop when the diff between avg_obj_val and best_obj_val is too small
                        # stop_on_small_pop_diff=min_pop_diff,
                        # stop_on_no_improvements_gen_10=min_pop_diff,
                        stop_on_small_pop_variance=min_pop_variance,
                        crossover=crossover,
                        verbose=False)  # Will crash the jupyter notebook when turned on with many experiments

                evaluations += algo.evaluations
                if algo.exitflag == Exitflag.pop_converged:
                    print("Restart")
                    print("\t Evaluations", evaluations)
                    max_eval_variable = max_evaluations - evaluations
                    results['restart'] += 1
                else:
                    if verbose:
                        print("\tAVG_OBJ: ", algo.iter_avg_obj_val[-1])
                        print("\tBEST_OBJ:", algo.iter_best_obj_val[-1])
                        print("\tEVALUATIONS:", evaluations)
                    print(f"\tRUN DURATION: {time()-start_time}s")

                    results['avg_obj_vals'].append(algo.iter_avg_obj_val[-1])
                    results['best_obj_vals'].append(algo.iter_best_obj_val[-1])
                    results['evaluations'].append(evaluations)
                    results['exitflag'].append(algo.exitflag)

                    if algo.found_optimum:
                        results['optimum'] += 1
                    running = False
        return results


    start_time = time()
    seed(rng_seed)
    results = []
    for num_points in num_points_list:
        print("Num points: {}".format(num_points))
        dim = num_points*2

        popsize = get_popsize_func(dim)
        bounds = [[0, 1] for i in range(num_points*2)]
        init_bounds = get_init_bounds_func(num_points)
        pk = Packomania(num_points)
        optimum = pk.distance

        de = DifferentialEvolution(
            scattering_points,
            bounds,
            popsize,
            differential_weight,
            crossover_prob,
            init_bounds,
        )
        de.set_optimum(optimum, optimum_accuracy)
        r = _run(algo=de, max_evaluations=max_evaluations, min_pop_variance=min_pop_variance, crossover=crossover)
        results.append(r)

    print(f"Total time {time()-start_time}s")

    return results


