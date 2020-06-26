from numpy import load
import matplotlib.pyplot as plt
import numpy as np

DE = load('DE_BB_improve.npy')
AMaLGaM = load('AMaLGaM_benchmark_1.npy')
Pso = load('pso.npy')
RVGomea = load('RVGomea.npy')

data = np.array([DE, AMaLGaM, Pso, RVGomea])
labels = ['DE', 'AMaLGaM', 'PSO', 'GOMEA']
x = [2, 4, 5, 6, 7, 9]
vtrs = [10**3, 10**6]


def main():
    # print(data)
    fig, axs = plt.subplots(1, 2)
    for i, ax in enumerate(axs):
        ax.set_title("vtr = " + str(vtrs[i]))
        ax.set_yscale('log')
        for j, entry in enumerate(data):
            means = np.mean(entry[i], axis=1)
            # print("Means " + str(means))
            stddevs = np.std(entry[i], axis=1)
            # print("StdDevs " + str(stddevs))
            for k, stddev in enumerate(stddevs):
                if stddev > means[k] / 2:
                    stddevs[k] = means[k] / 1.2
            new_x = [entry+j*0.025 for entry in x]
            ax.errorbar(new_x, means, yerr=stddevs, label=labels[j])
            ax.set_ylabel('#Evaluations')
            ax.set_xlabel('#Circles')
            ax.legend()

    plt.show()


if __name__ == "__main__":
    # execute only if run as a script
    main()
