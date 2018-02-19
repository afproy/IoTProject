readChannelID = 426828; 
   

TemperatureFieldID = 3; 

readAPIKey = 'SGKWWOM1FXPZ4OFL'; 

temp = thingSpeakRead(readChannelID,'Fields',TemperatureFieldID,...
'DateRange', [datetime('Jan 31, 2018'),datetime('Mar 1, 2018')], 'ReadKey',readAPIKey); 

figure,
histogram(temp); 
xlabel('Temperature (°C)'); 
ylabel('Number of Measurements\newline for Each Temperature'); 
title('Histogram of Temperature Variation');
