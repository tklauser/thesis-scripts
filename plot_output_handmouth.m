% Mouth-Touching experiment: Plot the development of outputs over time
function [] = plot_output_handmouth(ddir)
clear all, close all;

% these parametes need to be manually adjusted to the experimental settings
nRows = 2;      % number of rows in the input image
nCols = 3;      % number of columns in the input image
nOutputsX = 2;  % number of output neurons coding x-axis movement
nOutputsY = 5;  % number of output neurons coding y-axis movement

if nargin < 1
    ddir = uigetdir('..', 'Select directory containing experiment log files');
    if (isequal(ddir, 0))
        disp('User canceled function');
        return
    end
end

nInputs = nRows * nCols;    % number of neurons in the input layer

for i=1:nInputs
    tmp = load(fullfile(ddir, sprintf('out_x_in_%d.log', i - 1)));
    % strip off time
    outputs_x(:,:,i) = tmp(:,2:end);
end

for i=1:nInputs
    tmp = load(fullfile(ddir, sprintf('out_y_in_%d.log', i - 1)));
    % strip off time
    outputs_y(:,:,i) = tmp(:,2:end);
end

[T, ~, ~] = size(outputs_x);

colormap Hot;
cmap = interp1(linspace(0, 1, size(colormap, 1)), colormap, linspace(0.0,0.9,T));
% reverse, so the more recent data points are darker
cmap = flipud(cmap);

plot_output_1d(T, nRows, nCols, nOutputsX, outputs_x, cmap);
figure;
plot_output_1d(T, nRows, nCols, nOutputsY, outputs_y, cmap);

% h = colorbar;
% set(h, 'Position', [ .8314 .11 .0581 .8150 ])
% for i=1:nInputs
%     pos = get(ax(i), 'Position');
%     set(ax(i), 'Position', [pos(1) pos(2) 0.85*pos(3) pos(4)]);
% end

end % function plot_output

function [] = plot_output_1d(T, nRows, nCols, nOutputs, outputs, cmap)

nInputs = nRows * nCols;
dt = max(floor(T / nInputs), 1);

for i=1:nInputs
    subplot(nRows, nCols, i);

    for t=1:dt:T
        hold on;

        lw = 0.5;
        if t == T || t + dt > T
            lw = 1.25;
        end

        plot(outputs(t,:,i), 'LineWidth', lw, 'Color', cmap(t,:));
        set(gca, 'FontSize', 8);
        set(gca, 'FontName', 'Times New Roman');
        if i > nCols
            xlabel('output unit', 'FontSize', 11);
        end
        if mod(i, nCols) == 1
            ylabel('activity', 'FontSize', 11);
        else
            set(gca, 'YTickLabel', [])
        end
        hold off;
    end
    axis([1 nOutputs -0.5 1.5]);
    axis square;
    set(gca,'XTick',1:nOutputs);
    if i > nInputs - nCols
        %set(gca,'XTickLabel',['0';' ';' ';' ';' ';' ';' ';' ';' ';'9']);
        set(gca,'XTickLabel',0:9);
    else
        set(gca,'XTickLabel',[]);
    end
    %title(sprintf('input x_{%d}', i - 1));
end

tightfig;

end % function plot_output_1d