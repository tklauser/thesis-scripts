close all;
clear all;

T=10;
fps=2;

vid = VideoWriter('quiver.avi');
vid.Quality = 100;
vid.FrameRate = fps;
open(vid);
for t=1:T
    [x,y] = meshgrid(-1.1:0.2:1.1);
    quiver(x,y*(-1)^t); axis equal;
    f = getframe(gcf);
    writeVideo(vid, f);
    M(t) = f;
    pause(1/fps);
end
close(vid);
%movie(M);