function force_fields()

clear all;
close all;

% parameters (many of these should be automatically determined from a file
% written by the Visumotor learning application)

nRows = 5;                % rows of the input image
nCols = 5;                % columns of the input image
nInputs = nRows * nCols;  % number of neurons in the input layer
nOutputs = 10;            % numver of neurons in the output layer
populationMin = -20.0;    % min (left) value of population coding
populationMax = 20;       % max (right) value of population coding

[xfile,xpath] = uigetfile({'*.log', 'Log files (comma separated)'}, 'Select weight log file for x-axis');
if (isequal(xfile, 0))
    disp('User canceled function');
    return
end

[yfile,ypath] = uigetfile({'*.log', 'Log files (comma separated)'}, 'Select weight log file for y-axis');
if (isequal(yfile, 0))
    disp('User canceled function');
    return
end

wx = load (fullfile(xpath,xfile));
wy = load (fullfile(ypath,yfile));

interval = (populationMax - populationMin) / (nOutputs - 1);
oMovement = (populationMin:interval:populationMax)'; % this should be read from a log file

oMovementx = oMovement;
oMovementy = oMovement;

time = wx(:,1);
wx = wx(:,2:end);
wy = wy(:,2:end);

size(wx)
size(wy)

T = length(time);

movex = zeros(T,1);
movey = zeros(T,1);

for t=1:T
    wxt = wx(t,:);
    wyt = wy(t,:);

    oTotalx = sum(wxt);
    oTotaly = sum(wyt);

    movex(t) = wxt * oMovementx ./ oTotalx;
    movey(t) = wyt * oMovementy ./ oTotaly;
end

plot([movex movey]);
