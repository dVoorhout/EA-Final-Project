clearvars; close all;

guidelines_A3 = readtable('Benchmark/BB_A3_v2.csv');
guidelines_A6 = readtable('Benchmark/BB_A6.csv');

paramsv3_A3 = readtable('Benchmark/BB_improv_A3_v3.csv'); % Best
paramsv4_A3 = readtable('Benchmark/BB_improv_A3_v4.csv');

NBB_bounds_A3 = readtable('Benchmark/NBB_improv_A3_bounds.csv');
NBB_bp_A3 = readtable('Benchmark/NBB_improv_A3_bp.csv');
NBB_full_A3 = readtable('Benchmark/NBB_improv_A3_full.csv');

paramsv2_A6 = readtable('Benchmark/BB_improv_A6_v2.csv'); % Best
paramsv3_A6 = readtable('Benchmark/BB_improv_A6_v3.csv'); 
paramsv4_A6 = readtable('Benchmark/BB_improv_A6_v4.csv');


paramsv2_A6_biggerNP = readtable('Benchmark/BB_improv_A6_v2_biggerNP.csv');

NBB_bounds_A6 = readtable('Benchmark/NBB_improv_A6_bounds.csv');
NBB_bp_A6 = readtable('Benchmark/NBB_improv_A6_bp.csv');
NBB_full_A6 = readtable('Benchmark/NBB_improv_A6_full.csv');


max_evals = 5e6;
y_max_evals_A3 = ones(size(guidelines_A3.num_points))*max_evals;
y_max_evals_A6 = ones(size(guidelines_A6.num_points))*max_evals;

%% Plot BB comparison A3
close all;
% Plot comparison
errorbar(guidelines_A3.num_points, guidelines_A3.mean_evaluations, guidelines_A3.std_evaluations)
hold on
errorbar(paramsv3_A3.num_points, paramsv3_A3.mean_evaluations, paramsv3_A3.std_evaluations)
errorbar(paramsv4_A3.num_points, paramsv4_A3.mean_evaluations, paramsv4_A3.std_evaluations)

% Plot maximum number of evaluations
plot(guidelines_A3.num_points, y_max_evals_A3, 'r-' ,'HandleVisibility','off')
hold off

set(gca, 'YScale', 'log')
xlabel('Number of points')
ylabel('Number of evaluations')
xlim([1.9 9.1])

legend('Guidlines', 'Config A1', 'Config A2', 'location','southeast');

%% Plot BB comparison A6
close all;
% Plot comparison
errorbar(guidelines_A6.num_points, guidelines_A6.mean_evaluations, guidelines_A6.std_evaluations)
hold on
errorbar(paramsv3_A6.num_points, paramsv3_A6.mean_evaluations, paramsv3_A6.std_evaluations)
errorbar(paramsv2_A6.num_points, paramsv2_A6.mean_evaluations, paramsv2_A6.std_evaluations)
errorbar(paramsv4_A6.num_points, paramsv4_A6.mean_evaluations, paramsv4_A6.std_evaluations)

% Plot maximum number of evaluations
plot(guidelines_A6.num_points, y_max_evals_A6, 'r-' ,'HandleVisibility','off')
hold off

set(gca, 'YScale', 'log')
xlabel('Number of points')
ylabel('Number of evaluations')
xlim([1.9 9.1])

legend('Guidlines', 'Config B1', 'Config B2', 'Config B3', 'location','southeast');

%% Plot NBB comparison A3
close all;

errorbar(paramsv3_A3.num_points, paramsv3_A3.mean_evaluations, paramsv3_A3.std_evaluations)
hold on;
errorbar(NBB_bounds_A3.num_points, NBB_bounds_A3.mean_evaluations, NBB_bounds_A3.std_evaluations)
errorbar(NBB_bp_A3.num_points, NBB_bp_A3.mean_evaluations, NBB_bp_A3.std_evaluations)
errorbar(NBB_full_A3.num_points, NBB_full_A3.mean_evaluations, NBB_full_A3.std_evaluations)
plot(guidelines_A3.num_points, y_max_evals_A3, 'r-' ,'HandleVisibility','off')
hold off

set(gca, 'YScale', 'log')
xlabel('Number of points')
ylabel('Number of evaluations')
xlim([1.9 9.1])

legend('BB', 'NBB better init', 'NBB better crossover', 'NBB full', 'location','southeast');

%% Plot NBB comparison A6
close all;

errorbar(paramsv2_A6.num_points, paramsv2_A6.mean_evaluations, paramsv2_A6.std_evaluations)
hold on;
errorbar(paramsv2_A6_biggerNP.num_points, paramsv2_A6_biggerNP.mean_evaluations, paramsv2_A6_biggerNP.std_evaluations)
errorbar(NBB_bounds_A6.num_points, NBB_bounds_A6.mean_evaluations, NBB_bounds_A6.std_evaluations)
errorbar(NBB_bp_A6.num_points, NBB_bp_A6.mean_evaluations, NBB_bp_A6.std_evaluations)
errorbar(NBB_full_A6.num_points, NBB_full_A6.mean_evaluations, NBB_full_A6.std_evaluations)
plot(guidelines_A6.num_points, y_max_evals_A6, 'r-' ,'HandleVisibility','off')
hold off

set(gca, 'YScale', 'log')
xlabel('Number of points')
ylabel('Number of evaluations')
xlim([1.9 9.1])

legend('BB', 'BB bigger NP','NBB better init', 'NBB better crossover', 'NBB full', 'location','southeast');
