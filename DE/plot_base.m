clearvars; close all;

base_acc_3 = readtable('Baseline/num_points_9_0.001_base.csv');
base_acc_6 = readtable('Baseline/num_points_9_1e-06_base.csv');

packomania_table = read_packomania('Packomania/distance.txt');
pk_dist = get_packomania_dist(packomania_table, base_acc_3.num_points);

max_evals = 5e6;


%% Plot base for 1e-3 accuracy
% Plot mean evaluations
close all
plot_evals(base_acc_3, max_evals)

figure()
plot_d_best_obj_val(base_acc_3, pk_dist, 1e-3)

figure()
plot_d_avg_obj_val(base_acc_3, pk_dist, 1e-3)


%% Plot base for 1e-6 accuracy
% Plot mean evaluations
close all
plot_evals(base_acc_6, max_evals)

figure()
plot_d_best_obj_val(base_acc_6, pk_dist, 1e-6)

figure()
plot_d_avg_obj_val(base_acc_6, pk_dist, 1e-6)




%% Functions

function plot_evals(results, max_evals)
% Plot evals
y_max_evals = ones(size(results.num_points))*max_evals;
yyaxis left
errorbar(results.num_points, results.mean_evaluations, results.std_evaluations)
hold on;
plot(results.num_points, y_max_evals, 'r-' ,'HandleVisibility','off')
hold off

xlabel('Number of points')
ylabel('Number of evaluations')
set(gca, 'YScale', 'log')

% Plots VTR reached count
yyaxis right
plot(results.num_points, results.VTR_reached_count, 'x')
ylim([-0.5 10.5])
ylabel('VTR reached count')
xlim([1.9 9.1])
end

function plot_d_best_obj_val(results, pk_dist, accuracy)
y_accuracy = ones(size(results.num_points))*accuracy;

yyaxis left
errorbar(results.num_points, pk_dist-results.mean_best_obj_vals, results.std_best_obj_vals)

hold on;
plot(results.num_points, y_accuracy)
hold off
ylabel('Best objective value deviation from VTR')

yyaxis right
plot(results.num_points, results.VTR_reached_count, 'x')
ylim([-0.5 10.5])
ylabel('VTR reached count')

xlim([1.9 9.1])
xlabel('Number of points')
end

function plot_d_avg_obj_val(results, pk_dist, accuracy)
y_accuracy = ones(size(results.num_points))*accuracy;

yyaxis left
errorbar(results.num_points, pk_dist-results.mean_avg_obj_vals, results.std_avg_obj_vals)

hold on;
plot(results.num_points, y_accuracy)
hold off
ylabel('Average objective value deviation from VTR')
set(gca, 'YScale', 'log')

yyaxis right
plot(results.num_points, results.VTR_reached_count, 'x')
ylim([-0.5 10.5])
ylabel('VTR reached count')

xlim([1.9 9.1])
xlabel('Number of points')
end


function packomania = read_packomania(filename)
packomania = readtable(filename);
packomania.Properties.VariableNames = {'circles','distance'};
end

function dist = get_packomania_dist(packomania, num_circles)
dist = zeros(size(num_circles));
for i=1:length(num_circles)
    dist(i) = table2array(packomania(find(packomania.circles == num_circles(i)), 'distance'));
end
end
