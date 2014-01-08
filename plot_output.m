% Plot the development of outputs over time
function [] = plot_output(ddir)

clear all, close all;

nRows = 1;
nCols = 5;
nOutputs = 10;

if nargin < 1
    ddir = uigetdir('..', 'Select directory containing experiment log files');
    if (isequal(ddir, 0))
        disp('User canceled function');
        return
    end
end

ddir

% if we have a file specifying the parameters, use them from there
if exist(fullfile(ddir, 'params.log'), 'file') == 2
    params = dlmread(fullfile(ddir, 'params.log'), ',', 1, 0);
    % only use complete parameter set
    if length(params) >= 4
        p = num2cell(params);
        % first entry is time, because of the file format -> ignore
        [~, nRows, nCols, nOutputs] = p{1:4};
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

T = T -1;
plot_output_1d(T, nRows, nCols, nOutputs, outputs_x, cmap);
figure;
plot_output_1d(T, nRows, nCols, nOutputs, outputs_y, cmap);

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

N = 1;
if mod(nInputs, 7) == 0
    N = 7;
elseif mod(nInputs, 5) == 0
    N = 5;
elseif mod(nInputs, 3) == 0
    N = 3;
end

for i=1:nInputs
    subplot(N, nInputs/N, nInputs - i + 1);

    for t=1:dt:T
        hold on;

        lw = 0.5;
        if t == T || t + dt > T
            lw = 1.25;
        end

        plot(outputs(t,:,i), 'LineWidth', lw, 'Color', cmap(t,:));
        set(gca, 'FontSize', 8);
        set(gca, 'FontName', 'Times New Roman');
        if i <= nCols
            xlabel('output unit', 'FontSize', 11);
        end
        if mod(i, nCols) == 0
            ylabel('activity', 'FontSize', 11);
        else
            set(gca, 'YTickLabel', [])
        end
        hold off;
    end
    axis([1 nOutputs -0.5 2.75]);
    axis square;
    set(gca,'XTick',1:10);
    if i <= nCols
        %set(gca,'XTickLabel',['0';' ';' ';' ';' ';' ';' ';' ';' ';'9']);
        set(gca,'XTickLabel',0:9);
    else
        set(gca,'XTickLabel',[]);
    end
    %title(sprintf('input x_{%d}', i - 1));
end

tightfig;

end % function plot_output_1d
