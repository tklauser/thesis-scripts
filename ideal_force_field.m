% "Ideal" force field to result in fixating behavior
function [u,v] = ideal_force_field(minX, maxX, minY, maxY)
    x = linspace(minX,maxX,5)*(-1);
    y = linspace(minY,maxY,5);
    [u,v] = meshgrid(x,y);
    u = flipud(u);
    v = flipud(v);
end % function
