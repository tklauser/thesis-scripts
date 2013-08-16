% "Ideal" force field to result in fixating behavior
function [u,v] = ideal_force_field(minX, maxX, minY, maxY, nRows, nCols)
    % if not specified use default values of 5 for nRows and nCols
    if nargin < 6
        nRows = 5;
        nCols = 5;
    end

    x = linspace(minX,maxX,nCols)*(-1);
    y = linspace(minY,maxY,nRows);
    [u,v] = meshgrid(x,y);
    u = flipud(u);
    v = flipud(v);
end % function
