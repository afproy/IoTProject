readChannelID = 426828; 
   
HumidityFieldID = 1; 
TemperatureFieldID = 3;

readAPIKey = 'SGKWWOM1FXPZ4OFL'; 

   
humi = thingSpeakRead(readChannelID,'Fields',HumidityFieldID,...
'DateRange', [datetime('Jan 31, 2018'),datetime('Mar 1, 2018')], 'ReadKey',readAPIKey);
temp = thingSpeakRead(readChannelID,'Fields',TemperatureFieldID,...
'DateRange', [datetime('Jan 31, 2018'),datetime('Mar 1, 2018')], 'ReadKey',readAPIKey);

temp(isnan(temp)) = [];
humi(isnan(humi)) = [];

humi_length = length(humi)
temp_length = length(temp)
if humi_length > temp_length
    humi = humi(1:temp_length)
    humi_length = temp_length
elseif humi_length < temp_length
    temp = temp(1:humi_length)
    temp_length = humi_length
end

a = 6.1121;
b = 18.678;
c = 257.14;
d = 234.5;

gamma = log(humi/100)+(b*temp)./(c+temp);
dew_point = (c*gamma)./(b-gamma)

figure,
plot(dew_point);
hold on,
plot(temp);
xlabel('Time'); 
ylabel('Dew point (C)'); 
title('Dew point time evolution');

% freeboard iframe=<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/210501"></iframe>
