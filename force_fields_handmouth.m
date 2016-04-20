% Quiver plot of the development of weights over time
function [dx,dy] = force_fields_handmouth(ddir)
clear all, close all;

% these parametes need to be manually adjusted to the experimental settings
nRows = 2;      % number of rows in the input image
nCols = 3;      % number of columns in the input image
nOutputsX = 5;  % number of output neurons coding x-axis movement
nOutputsY = 2;  % number of output neurons coding y-axis movement
movementMinX = -2;
movementMaxX = 2;
movementMinY = 1;
movementMaxY = 2;

% video parameters
videoQuality = 100;
videoFPS = 4;

if nargin < 1
    ddir = uigetdir('..', 'Select directory containing experiment log files');
    if (isequal(ddir, 0))
        disp('User canceled function');
        return
    end
end

nInputs = nRows * nCols;    % number of neurons in the input layer

% ATTENTION: x and y axis got twisted in the control program, thus we
% change them here
xfiles = dir(fullfile(ddir, 'weights_y_in*.log'));
yfiles = dir(fullfile(ddir, 'weights_x_in*.log'));
nx = length(xfiles);
ny = length(yfiles);

% assume number of neurons equal for x and y, otherwise the
% rest of the script won't work
if nx == 0 || ny == 0 || nx ~= nInputs || nx ~= ny
    disp('There is something wrong with your data directory:');
    fprintf(1, '# of files for x: %d', nx);
    fprintf(1, '# of files for y: %d', ny);
    fprintf(1, '# of inputs: %d', nInputs);
    return
end

% files don't necessarily get listed in numerical correct order,
% thus extract the input index from the file name using a regexp
for i=1:nx
    num = regexp(xfiles(i).name, 'weights_y_in_(\d+).*\.log', 'tokens');
    % index + 1 since indices start at 1, not 0 in MATLAB
    n = str2double(num{1}) + 1;
    Wx(:,:,n) = load(fullfile(ddir, xfiles(i).name));
end

for i=1:ny
    num = regexp(yfiles(i).name, 'weights_x_in_(\d+).*\.log', 'tokens');
    % index + 1 since indices start at 1, not 0 in MATLAB
    n = str2double(num{1}) + 1;
    Wy(:,:,n) = load(fullfile(ddir, yfiles(i).name));
end

intervalX = (movementMaxX - movementMinX) / (nOutputsX - 1);
intervalY = (movementMaxY - movementMinY) / (nOutputsY - 1);
oMovementX = (movementMinX:intervalX:movementMaxX)';
oMovementY = (movementMinY:intervalY:movementMaxY)';
time = Wx(:,1,1);
T = length(time);

figure(1);

% plot movements for each of the neurons
for i=1:nInputs
    wx = Wx(:,2:end,i);
    wy = Wy(:,2:end,i);

    movex = zeros(T,1);
    movey = zeros(T,1);

    for t=1:T
        wxt = wx(t,:);
        wyt = wy(t,:);

        [ ~, amx ] = max(wxt, [], 2);
        [ ~, amy ] = max(wyt, [], 2);

        movex(t) = oMovementX(amx);
        movey(t) = oMovementY(amy);
    end

    subplot(nRows, nCols, i);
    plot([movex movey]);
    title(sprintf('neuron %d', i - 1));
end

% prepare video creation
vidFile = sprintf('handmouth_force_field_%s.avi', date);
vid = VideoWriter(fullfile(ddir, vidFile));
vid.Quality = videoQuality;
vid.FrameRate = videoFPS;
open(vid);

figure(2);

step = 1; ff = 0;
%T=50*nInputs;

%T = 2*nInputs;

for t=1:T
    if ff
        t = T;
    end
    
    dx = zeros(nx, 1);
    dy = zeros(ny, 1);

    maxx = zeros(nInputs, 1);
    maxy = zeros(nInputs, 1);

    for i=1:nInputs
        wxt = Wx(t,2:end,i);
        [ ~, amx ] = max(wxt, [], 2);
        dx(i) = oMovementX(amx);
        
        maxx(i) = amx - 1;
    end
    for i=1:nInputs
        wyt = Wy(t,2:end,i);
        [ ~, amy ] = max(wyt, [], 2);
        dy(i) = oMovementY(amy);
        
        maxy(i) = amy - 1;
    end

%    maxx = reshape(maxx, nCols, nRows)'
%    maxy = flipud(reshape(maxy, nCols, nRows)')

    % convert to matrix
    dx = reshape(dx, nCols, nRows)' * -1;
    dy = fliplr(flipud(reshape(dy, nCols, nRows)' * -1));
    
%    [ 1 -1 -1; 1 -1 -1]
%    [ 2 1 1; 2 2 2] * -1

    % for each time step build up a quiver plot
    quiver(dx,dy, 'LineWidth', 2.0);
    set(gca, 'FontSize', 20);
    set(gca, 'FontName', 'Times New Roman');
%    axis square;
    axis([0.5,nCols+0.5,0.25,nRows+0.5]);
    set(gca, 'XTick', 0:nCols);
    set(gca, 'YTick', 0:nRows);
    set(gca, 'XTickLabel', -1:nCols-1);
    set(gca, 'YTickLabel', nRows:-1:0);

    f = getframe(2);
    writeVideo(vid, f);
    %pause(1/4);
    
    if ff
        return
    end

    if step == 1
        ret = input('Select action: [s]tep, [c]ontinue, [f]ast forward, [q]uit: ', 's');
        if ret == 's'
            step = 1;
        elseif ret == 'c'
            step = 0;
        elseif ret == 'f'
            step = 0;
            ff = 1;
        elseif ret == 'q'
            return
        else
            disp('invalid input');
        end
    end
end

close(vid);

end % function force_fields_handmouth