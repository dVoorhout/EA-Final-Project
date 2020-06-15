import subprocess
import numpy as np
import time

result_file_name = 'best_generation_final.dat'
distances_file = 'distance.txt'
number_of_circles = [2, 4, 5, 6, 7, 9]
number_of_evaluations = 1e7
allowed_variance = 0
vtr = 1e-6
number_of_runs = 10


def main():

    all_circles_np_array_results = np.zeros((6, 10))
    for i, current_number_of_circles in enumerate(number_of_circles):
        evaluations_of_each_run = []

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
                cmd = "AMaLGaM.exe -s -v -r -g 13 " + str(current_number_of_circles * 2) + \
                      " 0 1 0 3.5e-1 50 1 9e-1 1 " + str(number_of_evaluations) + " " + str(vtr) + \
                      " 35 " + str(allowed_variance) + " " + str(1/benchmark_distance)
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
                if difference - vtr <= 1e-7:
                    print("Done with this run!")
                    done_with_run = True
                    print("Total used evals for this run: " + str(total_used_evaluations_in_run) +
                          ", done using " + str(restart_count) + " restarts")
                    evaluations_of_each_run.append(total_used_evaluations_in_run)

                restart_count += 1

        all_circles_np_array_results[i] = evaluations_of_each_run

    print("-----------------------------------------------------------------")
    print(all_circles_np_array_results)
    print(np.mean(all_circles_np_array_results, axis=1))
    # print("Problem of " + str(number_of_circles) + " circles solved with a precision of " +
    #       str(vtr) + " using on average " + str(total_evaluations / number_of_runs) +
    #       " evaluations over " + str(number_of_runs) + " runs")


if __name__ == "__main__":
    # execute only if run as a script
    main()
