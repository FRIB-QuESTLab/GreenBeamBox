function z = cscope(a,b,n,T0,dt,TrigSecs,TrigPartSecs,Frame)
y = a
figure (1) % Plot data to fig 1
specgram(a,512,1/dt,500,475)
title('Spectrogram') 