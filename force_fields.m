% Quiver plot of the development of weights over time
function force_fields(ddir)

% parameters

videoQuality = 100;
videoFPS = 4;
plot_cols = 5;            % number of columns in the plot

% experiment default values, can be overriden by params.log
nRows = 5;                  % rows of the input image
nCols = 5;                  % columns of the input image
nInputs = nRows * nCols;    % number of neurons in the input layer
nOutputs = 10;              % number of neurons in the output layer
populationMinX = -20.0;     % min (left) X value of population coding
populationMaxX = 20;        % max (right) X value of population coding
populationMinY = -20.0;     % min (left) Y value of population coding
populationMaxY = 20;        % max (right) Y value of population coding

if nargin < 1
    ddir = uigetdir('..', 'Select directory containing experiment log files');
    if (isequal(ddir, 0))
        disp('User canceled function');
        return
    end
end

% if we have a file specifying the parameters, use them from there
if exist(fullfile(ddir, 'params.log'), 'file') == 2
    params = importdata(fullfile(ddir, 'params.log'), ',', 1);
    % only use complete parameter set
    if length(params.data) == 8
        pCells = num2cell(params.data);
        % first entry is time, because of the file format -> ignore
        [~, nRows, nCols, nOutputs, ...
            populationMinX, populationMaxX, ...
            populationMinY, populationMaxY] = pCells{:};
    end
end

% take date from directory name
[~, date, ~] = fileparts(ddir);

xfiles = dir(fullfile(ddir, 'weights_x_in*.log'));
yfiles = dir(fullfile(ddir, 'weights_y_in*.log'));
nx = length(xfiles);
ny = length(yfiles);

% assume number of neurons equal for x and y, otherwise the
% rest of the script won't work
if nx == 0 || ny == 0 || nx ~= nInputs || nx ~= ny
    disp('There is something wrong with your data directory:');
    disp(sprintf('# of files for x: %d', nx));
    disp(sprintf('# of files for y: %d', ny));
    return
end

% files don't necessarily get listed in numerical correct order,
% thus extract the input index from the file name using a regexp
for i=1:nx
    num = regexp(xfiles(i).name, 'weights_x_in_(\d+).*\.log', 'tokens');
    % index + 1 since indices start at 1, not 0 in MATLAB
    n = str2double(num{1}) + 1;
    Wx(:,:,n) = importdata(fullfile(ddir, xfiles(i).name));
end

for i=1:ny
    num = regexp(yfiles(i).name, 'weights_y_in_(\d+).*\.log', 'tokens');
    % index + 1 since indices start at 1, not 0 in MATLAB
    n = str2double(num{1}) + 1;
    Wy(:,:,n) = importdata(fullfile(ddir, yfiles(i).name));
end

intervalX = (populationMaxX - populationMinX) / (nOutputs - 1);
intervalY = (populationMaxY - populationMinY) / (nOutputs - 1);
oMovementX = (populationMinX:intervalX:populationMaxX)';
oMovementY = (populationMinY:intervalY:populationMaxY)';

time = Wx(:,1,1);
T = length(time);

figure(1);

% plot movements for each of the neurons
for i=1:nx
    wx = Wx(:,2:end,i);
    wy = Wy(:,2:end,i);

    movex = zeros(T,1);
    movey = zeros(T,1);

    for t=1:T
        wxt = wx(t,:);
        wyt = wy(t,:);

        oTotalX = sum(wxt);
        oTotalY = sum(wyt);

        movex(t) = wxt * oMovementX ./ oTotalX;
        movey(t) = wyt * oMovementY ./ oTotalY;
    end

    subplot(ceil(nx/plot_cols), plot_cols, i);
    plot([movex movey]);
end

% prepare video creation
vidFile = sprintf('force_field_%s.avi', date);
vid = VideoWriter(fullfile(ddir, vidFile));
vid.Quality = videoQuality;
vid.FrameRate = videoFPS;
open(vid);

figure(2);

for t=1:T
    dx = zeros(nx, 1);
    dy = zeros(nx, 1);    
    
    for i=1:nx
        wxt = Wx(t,2:end,i);
        wyt = Wy(t,2:end,i);
        
        oTotalX = sum(wxt);
        oTotalY = sum(wyt);
        
        dx(i) = wxt * oMovementX ./ oTotalX;
        dy(i) = wyt * oMovementY ./ oTotalY;
    end

    dx = reshape(dx, nRows, nCols);
    dy = reshape(dy, nRows, nCols);
    
    % flip up to down since 0,0 is the input neuron for the upper left
    % corner
    dx = flipud(dx);
    dy = flipud(dy);
    
    % for each time step build up a quiver plot
    quiver(dx,dy);
    axis square;
    axis([0,nCols+1,0,nRows+1]);
    f = getframe(2);
    writeVideo(vid, f);
    pause(1/4);
end

close(vid);

end % function force_fields()