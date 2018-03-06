readChannelID = 426828; 
   
HumidityFieldID = 1; 
   
readAPIKey = 'SGKWWOM1FXPZ4OFL'; 

   
humi = thingSpeakRead(readChannelID,'Fields',HumidityFieldID,...
'DateRange', [datetime('Jan 31, 2018'),datetime('Jan 31, 2019')], 'ReadKey',readAPIKey); 
   
histogram(humi); 
xlabel('Humidity (%)'); 
ylabel('Number of Measurements\newline for Each Humidity'); 
title('Histogram of Humidity Variation');
% freeboard iframe=<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/210295"></iframe>
