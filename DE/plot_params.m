clearvars; close all;

CR_num_points_9_A3 = readtable('Params/num_points_9_0.001_CR2.csv');
NP_num_points_9_A3 = readtable('Params/num_points_9_0.001_NP.csv');
F_num_points_9_A3 = readtable('Params/num_points_9_0.001_F.csv');


CR_num_points_6_A3 = readtable('Params/num_points_6_0.001_CR2.csv');
NP_num_points_6_A3 = readtable('Params/num_points_6_0.001_NP.csv');
F_num_points_6_A3 = readtable('Params/num_points_6_0.001_F.csv');

CR_num_points_3_A3 = readtable('Params/num_points_3_0.001_CR2.csv');
NP_num_points_3_A3 = readtable('Params/num_points_3_0.001_NP.csv');
F_num_points_3_A3 = readtable('Params/num_points_3_0.001_F.csv');

CR_num_points_3_A6 = readtable('Params/num_points_3_1e-06_CR2.csv');
NP_num_points_3_A6 = readtable('Params/num_points_3_1e-06_NP.csv');
F_num_points_3_A6 = readtable('Params/num_points_3_1e-06_F.csv');


packomania_table = read_packomania('Packomania/distance.txt');
pk_dist_3 = get_packomania_dist(packomania_table, 3);
pk_dist_6 = get_packomania_dist(packomania_table, 6);
pk_dist_9 = get_packomania_dist(packomania_table, 9);

max_evals = 5e6;
accuracy_A3 = 1e-3;
accuracy_A6 = 1e-6;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Influence CR Points 9 A3
close all;
plot_evals(CR_num_points_9_A3, max_evals, 'Crossover rate')
figure()
plot_d_avg_obj_val(CR_num_points_9_A3, pk_dist_9, accuracy_A3, 'Crossover rate');

%% Influence NP Points 9 A3
close all;
plot_evals(NP_num_points_9_A3, max_evals, 'Population size')
figure()
plot_d_avg_obj_val(NP_num_points_9_A3, pk_dist_9, accuracy_A3, 'Population size');

%% Influence F Points 9 A3
close all;
plot_evals(F_num_points_9_A3, max_evals, 'Differential weight')
figure()
plot_d_avg_obj_val(F_num_points_9_A3, pk_dist_9, accuracy_A3, 'Differential weight');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Influence CR Points 6 A3
close all;
plot_evals(CR_num_points_6_A3, max_evals, 'Crossover rate')
figure()
plot_d_avg_obj_val(CR_num_points_6_A3, pk_dist_6, accuracy_A3, 'Crossover rate');

%% Influence NP Points 6 A3
close all;
plot_evals(NP_num_points_6_A3, max_evals, 'Population size')
figure()
plot_d_avg_obj_val(NP_num_points_6_A3, pk_dist_6, accuracy_A3, 'Population size');

%% Influence F Points 6 A3
close all;
plot_evals(F_num_points_6_A3, max_evals, 'Differential weight')
figure()
plot_d_avg_obj_val(F_num_points_6_A3, pk_dist_6, accuracy_A3, 'Differential weight');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Influence CR Points 3 A3
close all;
plot_evals(CR_num_points_3_A3, max_evals, 'Crossover rate')
figure()
plot_d_avg_obj_val(CR_num_points_3_A3, pk_dist_3, accuracy_A3, 'Crossover rate');


%% Influence NP Points 3 A3
close all;
plot_evals(NP_num_points_3_A3, max_evals, 'Population size')
figure()
plot_d_avg_obj_val(NP_num_points_3_A3, pk_dist_3, accuracy_A3, 'Population size');

%% Influence F Points 3 A3
close all;
plot_evals(F_num_points_3_A3, max_evals, 'Differential weight')
figure()
plot_d_avg_obj_val(F_num_points_3_A3, pk_dist_3, accuracy_A3, 'Differential weight');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Influence CR Points 3 A6
close all;
plot_evals(CR_num_points_3_A6, max_evals, 'Crossover rate')
figure()
plot_d_avg_obj_val(CR_num_points_3_A6, pk_dist_3, accuracy_A6, 'Crossover rate');


%% Influence NP Points 3 A6
close all;
plot_evals(NP_num_points_3_A6, max_evals, 'Population size')
figure()
plot_d_avg_obj_val(NP_num_points_3_A6, pk_dist_3, accuracy_A6, 'Population size');
%% Influence F Points 3 A6
close all;
plot_evals(F_num_points_3_A6, max_evals, 'Differential weight')
figure()
plot_d_avg_obj_val(F_num_points_3_A6, pk_dist_3, accuracy_A6, 'Differential weight');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Influence CR A3
close all
plot_comp(CR_num_points_3_A3, CR_num_points_6_A3, CR_num_points_9_A3, max_evals, 'Crossover rate')

%% Influence F A3
close all
plot_comp(F_num_points_3_A3, F_num_points_6_A3, F_num_points_9_A3, max_evals, 'Differential weight')

%% Influence NP A3
close all
plot_comp_NP(NP_num_points_3_A3, NP_num_points_6_A3, NP_num_points_9_A3, max_evals, 'Population size')


%% functions

function plot_comp(num_points_3, num_points_6, num_points_9, max_evals, xname)
y_max_evals = ones(size(num_points_3.x))*max_evals;
yyaxis left

errorbar(num_points_9.x, num_points_9.mean_evaluations, num_points_9.std_evaluations)
hold on 
errorbar(num_points_6.x, num_points_6.mean_evaluations, num_points_6.std_evaluations)
errorbar(num_points_3.x, num_points_3.mean_evaluations, num_points_3.std_evaluations)
plot(num_points_3.x, y_max_evals, 'r-' ,'HandleVisibility','off')
hold off
set(gca, 'YScale', 'log')
ylabel('Number of evaluations')

yyaxis right
plot(num_points_9.x, num_points_9.VTR_reached_count, 'x')
hold on 
plot(num_points_6.x, num_points_6.VTR_reached_count, 'o')
plot(num_points_3.x, num_points_3.VTR_reached_count, '+')
hold off
ylim([-0.5 10.5])
ylabel('VTR reached count')

legend('','','', '#points 9', '#points 6', '#points 3',...
      'Location', 'southwest', 'NumColumns', 2)

xlabel(xname)

xlim([num_points_3.x(1)-0.05*num_points_3.x(end) ...
    num_points_3.x(end)+0.05*num_points_3.x(end)])
end

function plot_comp_NP(num_points_3, num_points_6, num_points_9, max_evals, xname)
x = 1:length(num_points_3.x);
y_max_evals = ones(size(x))*max_evals;

yyaxis left
errorbar(x, num_points_9.mean_evaluations, num_points_9.std_evaluations)
hold on 
errorbar(x, num_points_6.mean_evaluations, num_points_6.std_evaluations)
errorbar(x, num_points_3.mean_evaluations, num_points_3.std_evaluations)
plot(x, y_max_evals, 'r-' ,'HandleVisibility','off')
hold off
set(gca, 'YScale', 'log')
ylabel('Number of evaluations')

yyaxis right
plot(x, num_points_9.VTR_reached_count, 'x')
hold on 
plot(x, num_points_6.VTR_reached_count, 'o')
plot(x, num_points_3.VTR_reached_count, '+')
hold off
ylim([-0.5 10.5])
ylabel('VTR reached count')

xticks([1 2 3 4 5])
xticklabels({'D', '5D', '10D', '15D', '20D'})

legend('','','', '#points 9', '#points 6', '#points 3',...
      'Location', 'southwest', 'NumColumns', 2)

xlabel(xname)

xlim([x(1)-0.05*x(end) ...
    x(end)+0.05*x(end)])
end


function plot_evals(results, max_evals, xname)
% Plot evals
y_max_evals = ones(size(results.x))*max_evals;
yyaxis left
errorbar(results.x, results.mean_evaluations, results.std_evaluations)
hold on;
plot(results.x, y_max_evals, 'r-' ,'HandleVisibility','off')
hold off

xlabel(xname)
ylabel('Number of evaluations')
set(gca, 'YScale', 'log')

% Plots VTR reached count
yyaxis right
plot(results.x, results.VTR_reached_count, 'x')
ylim([-0.5 10.5])
ylabel('VTR reached count')
xlim([results.x(1)-0.05*results.x(end) results.x(end)+0.05*results.x(end)])
end

function plot_d_best_obj_val(results, pk_dist, accuracy)
y_accuracy = ones(size(results.num_points))*accuracy;

yyaxis left
errorbar(results.num_points, pk_dist-results.mean_best_obj_vals, results.std_best_obj_vals)

hold on;
plot(results.num_points, y_accuracy)
hold off
ylabel('Objective value deviation from VTR')

yyaxis right
plot(results.num_points, results.VTR_reached_count, 'x')
ylim([-0.5 10.5])
ylabel('VTR reached count')

xlim([results.x(1)-0.05*results.x(end) results.x(end)+0.05*results.x(end)])
xlabel('Number of points points')
end

function plot_d_avg_obj_val(results, pk_dist, accuracy, xname)
y_accuracy = ones(size(results.x))*accuracy;

yyaxis left
errorbar(results.x, pk_dist-results.mean_avg_obj_vals, results.std_avg_obj_vals)

hold on;
plot(results.x, y_accuracy)
hold off
ylabel('Objective value deviation from VTR')
set(gca, 'YScale', 'log')

yyaxis right
plot(results.x, results.VTR_reached_count, 'x')
ylim([-0.5 10.5])
ylabel('VTR reached count')

xlim([results.x(1)-0.05*results.x(end) results.x(end)+0.05*results.x(end)])
xlabel(xname)
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