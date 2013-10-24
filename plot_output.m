% Plot the development of outputs over time
function [] = plot_output(ddir)

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

% if we have a file specifying the parameters, use them from there
% if exist(fullfile(ddir, 'params.log'), 'file') == 2
%     params = dlmread(fullfile(ddir, 'params.log'), ',', 1, 0);
%     % only use complete parameter set
%     if length(params) >= 4
%         p = num2cell(params);
%         % first entry is time, because of the file format -> ignore
%         [~, nRows, nCols, nOutputs] = p{1:4};
%     end
% end

nInputs = nRows * nCols;    % number of neurons in the input layer

for i=1:nInputs
    tmp = load(fullfile(ddir, sprintf('out_x_in_%d.log', i - 1)));
    % strip off time
    outputs(:,:,i) = tmp(:,2:end);
end

[T, ~, ~] = size(outputs);

for t=1:T
    for i=1:nInputs
        subplot(nInputs, 1, i);
        plot(outputs(t,:,i));
        axis([1.0 10.0 -1.0 1.0]);        
        title(sprintf('input %d', i - 1));       
    end

    pause(1);
end
