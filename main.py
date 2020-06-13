import subprocess

result_file_name = 'best_generation_final.dat'
distances_file = 'distance.txt'
number_of_circles = 10
number_of_evaluations = 1e7
allowed_variance = 0
vtr = 1e-6


def main():
    benchmark_distance = 0
    with open(distances_file, 'r') as answers:
        for j, line in enumerate(answers):
            if j == number_of_circles - 2:
                for k, entry in enumerate(line.split()):
                    if k == 1:
                        benchmark_distance = float(entry)

    cmd = "AMaLGaM.exe -s -v -r -g 13 " + str(number_of_circles * 2) + \
          " 0 1 0 3.5e-1 50 1 9e-1 1 " + str(number_of_evaluations) + " " + str(vtr) + \
          " 35 " + str(allowed_variance) + " " + str(1/benchmark_distance)
    subprocess.run(cmd, shell=True)
    best_distance = 0
    with open(result_file_name, 'r') as results:
        for line in results:
            for i, entry in enumerate(line.split()):
                if i == number_of_circles * 2:
                    best_distance = 1 / float(entry)

    print(best_distance)
    print(benchmark_distance)
    print("diff: " + str(abs(best_distance - benchmark_distance)))


if __name__ == "__main__":
    # execute only if run as a script
    main()
