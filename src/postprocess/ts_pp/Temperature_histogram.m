readChannelID = 426828; 
   

TemperatureFieldID = 3; 

readAPIKey = 'SGKWWOM1FXPZ4OFL'; 

temp = thingSpeakRead(readChannelID,'Fields',TemperatureFieldID,...
'DateRange', [datetime('Jan 31, 2018'),datetime('Jan 31, 2019')], 'ReadKey',readAPIKey); 

figure,
histogram(temp); 
xlabel('Temperature (°C)'); 
ylabel('Number of Measurements\newline for Each Temperature'); 
title('Histogram of Temperature Variation');
% freeb iframe=<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/210501"></iframe>
