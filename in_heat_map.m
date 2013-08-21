function in_heat_map(ddir)
% show a heat map of the number of times an input field has been active

if nargin < 1
    ddir = uigetdir('..', 'Select directory containing experiment log files');
    if (isequal(ddir, 0))
        disp('User canceled function');
        return
    end
end

% if we have a file specifying the parameters, use them from there
if exist(fullfile(ddir, 'params.log'), 'file') == 2
    params = dlmread(fullfile(ddir, 'params.log'), ',', 1, 0);
    % only use complete parameter set
    if length(params) >= 8
        p = num2cell(params);
        % first entry is time, because of the file format -> ignore
        [~, nRows, nCols] = p{1:3};
    end
end

in(:,:) = load(fullfile(ddir, 'in.log'));

time = in(:,1);
T = length(time);
in = in(:,2:end);

for t=2:T
    tin = in(1:t,:);
    
    % sum up per column
    incount = sum(tin);
    incount = reshape(incount,nRows,nCols)';

    heatmap(incount, [], [], '%d', 'TextColor', 'w', 'ColorBar', true);
    title(sprintf('timestep %d', t));
    pause(1/16);
end

end % function in_heat_map()