import subprocess
import numpy as np
import time
from numpy import save
from numpy import load


result_file_name = 'best_generation_final.dat'
distances_file = 'distance.txt'
number_of_circles = [2,4,5,6,7,9]
number_of_evaluations = 1e10
allowed_variance = 0
check_improvement_checkpoints = 50
vtrs = [10**-3, 10**-6]
number_of_runs = 10
pop_size_multipliers = 2
pop_size = 1
number_of_populations = 1

def main():
    all_results = np.zeros((len(vtrs), len(number_of_circles), number_of_runs))
    all_number_of_restarts = np.zeros((len(vtrs), len(number_of_circles)))
    for v, vtr in enumerate(vtrs):
        for i, current_number_of_circles in enumerate(number_of_circles):
            evaluations_of_each_run = []
            total_number_of_restarts = 0
            benchmark_distance = 0
            with open(distances_file, 'r') as answers:
                for j, line in enumerate(answers):
                    if j == current_number_of_circles - 2:
                        for k, entry in enumerate(line.split()):
                            if k == 1:
                                benchmark_distance = float(entry)

            for k in range(number_of_runs):
                done_with_run = False
                total_used_evaluations_in_run = 0
                restart_count = 0
                while not done_with_run:
                    time.sleep(1)
                    cmd = "AMaLGaM_WB.exe -s -v -r -g 13 " + str(current_number_of_circles * 2) + \
                          " 0 1 0 3.5e-1 " + str(pop_size) + " " + str(number_of_populations) + " 9e-1 1 " + str(number_of_evaluations) + " " + \
                          str(vtr) + " 35 " + str(allowed_variance) + " " + str(1/benchmark_distance) + " " + \
                          str(check_improvement_checkpoints) + " " + str(pop_size_multipliers)
                    subprocess.run(cmd, shell=True)
                    best_distance = 0
                    with open(result_file_name, 'r') as results:
                        for line in results:
                            for j, entry in enumerate(line.split()):
                                if j == current_number_of_circles * 2:
                                    best_distance = 1 / float(entry)
                                if j == current_number_of_circles * 2 + 2:
                                    used_number_of_evaluations = entry

                    print("Found distance: " + str(best_distance) + " in " + str(used_number_of_evaluations) + " evaluations")
                    print("Target distance: " + str(benchmark_distance))

                    difference = abs(best_distance - benchmark_distance)
                    print("Difference in distance: " + str(difference))
                    total_used_evaluations_in_run += int(used_number_of_evaluations)
                    if (difference - vtrs[0]) <= 10**-7:
                        print("Done with this run!")
                        done_with_run = True
                        print("Total used evals for this run: " + str(total_used_evaluations_in_run) +
                              ", done using " + str(restart_count) + " restarts")
                        evaluations_of_each_run.append(total_used_evaluations_in_run)

                    if not done_with_run:
                        restart_count += 1
                        total_number_of_restarts += 1

            all_results[v][i] = evaluations_of_each_run
            all_number_of_restarts[v][i] = total_number_of_restarts

    print("-----------------------------------------------------------------")
    print(all_results)
    print(np.mean(all_results, axis=2))
    print("total number of restarts used: ")
    print(str(all_number_of_restarts))

    save('Benchmark_AMaLGaM_WB_optimized_init_naive_greedy', all_results)
    save('Benchmark_AMaLGaM_WB_optimized_init_naive_greedy_#restarts', all_number_of_restarts)


    # print("Problem of " + str(number_of_circles) + " circles solved with a precision of " +
    #       str(vtr) + " using on average " + str(total_evaluations / number_of_runs) +
    #       " evaluations over " + str(number_of_runs) + " runs")


if __name__ == "__main__":
    # execute only if run as a script
    main()
