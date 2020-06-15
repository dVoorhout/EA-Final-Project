import subprocess

result_file_name = 'best_generation_final.dat'
distances_file = 'distance.txt'
number_of_circles = 10
number_of_evaluations = 1e7
allowed_variance = 1e-12
vtr = 1e-6
number_of_runs = 10


def main():
    benchmark_distance = 0
    with open(distances_file, 'r') as answers:
        for j, line in enumerate(answers):
            if j == number_of_circles - 2:
                for k, entry in enumerate(line.split()):
                    if k == 1:
                        benchmark_distance = float(entry)

    total_evaluations = 0
    for i in range(number_of_runs):
        done_with_run = False
        total_used_evaluations_in_run = 0
        restart_count = 0
        while not done_with_run:
            cmd = "AMaLGaM.exe -s -v -r -g 13 " + str(number_of_circles * 2) + \
                  " 0 1 0 3.5e-1 50 1 9e-1 1 " + str(number_of_evaluations) + " " + str(vtr) + \
                  " 35 " + str(allowed_variance) + " " + str(1/benchmark_distance)
            subprocess.run(cmd, shell=True)
            best_distance = 0
            with open(result_file_name, 'r') as results:
                for line in results:
                    for j, entry in enumerate(line.split()):
                        if j == number_of_circles * 2:
                            best_distance = 1 / float(entry)
                        if j == number_of_circles * 2 + 2:
                            used_number_of_evaluations = entry

            print("Found distance: " + str(best_distance) + " in " + str(used_number_of_evaluations) + " evaluations")
            print("Target distance: " + str(benchmark_distance))

            difference = abs(best_distance - benchmark_distance)
            print("Difference in distance: " + str(difference))
            total_used_evaluations_in_run += int(used_number_of_evaluations)
            if difference <= vtr:
                print("Done with this run!")
                done_with_run = True
                print("Total used evals for this run: " + str(total_used_evaluations_in_run) +
                      ", done using " + str(restart_count) + " restarts")
                total_evaluations += total_used_evaluations_in_run

            restart_count += 1

    print("-----------------------------------------------------------------")
    print("Problem of " + str(number_of_circles) + " circles solved with a precision of " +
          str(vtr) + " using on average " + str(total_evaluations / number_of_runs) +
          " evaluations over " + str(number_of_runs) + " runs")


if __name__ == "__main__":
    # execute only if run as a script
    main()
