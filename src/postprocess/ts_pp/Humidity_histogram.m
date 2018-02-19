readChannelID = 426828; 
   
HumidityFieldID = 1; 
   
readAPIKey = 'SGKWWOM1FXPZ4OFL'; 

   
humi = thingSpeakRead(readChannelID,'Fields',HumidityFieldID,...
'DateRange', [datetime('Jan 31, 2018'),datetime('Mar 1, 2018')], 'ReadKey',readAPIKey); 
   
histogram(humi); 
xlabel('Humidity (%)'); 
ylabel('Number of Measurements\newline for Each Humidity'); 
title('Histogram of Humidity Variation');
