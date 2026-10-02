function z = cscope(x,y,n,T0,dt,TrigSecs,TrigPartSecs,Frame)
% cscope1.m Plots the difference between two waveforms. You can plot one, two or three of them.
z=x-y; %return difference
time=((0:n-1)*dt)+T0; % Calc graph time axis

hold off %plot with persistance

plot(time, x, 'r', time, y, 'b', time, z, 'g') % Plot all signals or only one of them by commenting out the relevant lines. X and Y are offset by 2V 
% plot(time, x, 'r')
% plot(time, y, 'b')
% plot(time, z, 'g')

xlabel('Time')
ylabel('Voltage')
title('Channel A - B')
grid on


set(gcf,'Color',[0.3,0.7,0.2])
set(gcf, 'MenuBar', 'none')  %Will hide the Menu Bar
set(gcf, 'ToolBar', 'none')   %Will hide the Tool Bar
set(gcf,'NumberTitle','off') %don't show the figure number
set(gcf,'Name','Cleverscope Demo Matlab CS1') %select the name you want

