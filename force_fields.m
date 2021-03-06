% Quiver plot of the development of weights over time
function [dx,dy] = force_fields(ddir)

% parameters

videoQuality = 100;
videoFPS = 4;
plot_cols = 5;              % number of columns in the plot
wta = 1;                    % use winner-take-all to detemine resulting
                            % vector (instead of weighted sum)

% experiment default values, can be overriden by params.log
nRows = 5;                  % rows of the input image
nCols = 5;                  % columns of the input image
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
    params = dlmread(fullfile(ddir, 'params.log'), ',', 1, 0);
    % only use complete parameter set
    if length(params) >= 8
        p = num2cell(params);
        % first entry is time, because of the file format -> ignore
        [~, nRows, nCols, nOutputs, ...
            populationMinX, populationMaxX, ...
            populationMinY, populationMaxY] = p{1:8};
    end
end

nInputs = nRows * nCols;    % number of neurons in the input layer

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
    disp(sprintf('# of inputs: %d', nInputs));
    return
end

% files don't necessarily get listed in numerical correct order,
% thus extract the input index from the file name using a regexp
for i=1:nx
    num = regexp(xfiles(i).name, 'weights_x_in_(\d+).*\.log', 'tokens');
    % index + 1 since indices start at 1, not 0 in MATLAB
    n = str2double(num{1}) + 1;
    Wx(:,:,n) = load(fullfile(ddir, xfiles(i).name));
end

for i=1:ny
    num = regexp(yfiles(i).name, 'weights_y_in_(\d+).*\.log', 'tokens');
    % index + 1 since indices start at 1, not 0 in MATLAB
    n = str2double(num{1}) + 1;
    Wy(:,:,n) = load(fullfile(ddir, yfiles(i).name));
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

        if wta ~= 1
            oTotalX = sum(wxt);
            oTotalY = sum(wyt);

            movex(t) = wxt * oMovementX ./ oTotalX;
            movey(t) = wyt * oMovementY ./ oTotalY;
        else
            [ ~, amx ] = max(wxt, [], 2);
            [ ~, amy ] = max(wyt, [], 2);

            movex(t) = oMovementX(amx);
            movey(t) = oMovementY(amy);
        end
    end

    subplot(ceil(nx/plot_cols), plot_cols, i);
    plot([movex movey]);
    title(sprintf('neuron %d', i - 1));
end

% prepare video creation
vidFile = sprintf('force_field_%s.avi', date);
vid = VideoWriter(fullfile(ddir, vidFile));
vid.Quality = videoQuality;
vid.FrameRate = videoFPS;
open(vid);

figure(2);

step = 1; ff = 0;
[idealx,idealy] = ideal_force_field(-2,2,-2,2,nRows,nCols);
dideal = zeros(T,2);
dirideal = zeros(T,2);

for t=1:T
    if ff
        t = T;
    end
    
    dx = zeros(nx, 1);
    dy = zeros(nx, 1);

    for i=1:nx
        wxt = Wx(t,2:end,i);
        wyt = Wy(t,2:end,i);

        if wta ~= 1
            oTotalX = sum(wxt);
            oTotalY = sum(wyt);

            dx(i) = wxt * oMovementX ./ oTotalX;
            dy(i) = wyt * oMovementY ./ oTotalY;
        else
            [ ~, amx ] = max(wxt, [], 2);
            [ ~, amy ] = max(wyt, [], 2);

            dx(i) = oMovementX(amx);
            dy(i) = oMovementY(amy);
        end
    end

    % convert to matrix
    dx = reshape(dx, nRows, nCols);
    dy = reshape(dy, nRows, nCols);
    if nRows > 1
        % correct order row <-> columns
        dx = dx';
        dy = dy';
        % flip up to down since 0,0 is the input neuron for the upper left
        % corner. Invert x since positive value means movement to the left.
        dx = flipud(dx) * (-1.0);
        dy = flipud(dy);
    end

    % for each time step build up a quiver plot
    quiver(dx,dy, 'LineWidth', 2.0);
    axis square;
    axis([0,nCols+1,0,nRows+1]);
%    title(sprintf('step %d (t=%f)', t, Wx(t,1,1)));

%    dideal(t,1) = sum(sum(abs(dx - idealx)));
%    dideal(t,2) = sum(sum(abs(dy - idealy)));

    % compare direction to ideal direction
%    dirideal(t,1) = sum(sum(sign(dx) == sign(idealx)));
%    dirideal(t,2) = sum(sum(sign(dy) == sign(idealy)));

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

% figure(3);
% plot(dideal);
% legend('x dimension', 'y dimension');
% title('cum. diff. of actual force field to ideal force field');
% 
% figure(4)
% plot(dirideal);
% axis([0,T,0,nInputs]);
% legend('x dimension', 'y dimension');
% title('# of vectors with correct direction in x/y');

end % function force_fields()
