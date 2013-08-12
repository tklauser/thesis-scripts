function [u,v] = ideal_weights(minX, maxX, minY, maxY)
    x = linspace(minX,maxX,5)*(-1);
    y = linspace(minY,maxY,5);
    [u,v] = meshgrid(x,y);
    u = flipud(u);
    v = flipud(v);
end % function