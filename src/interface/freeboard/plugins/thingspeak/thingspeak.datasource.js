// ┌────────────────────────────────────────────────────────────────────┐ \\
// │ F R E E B O A R D                                                  │ \\
// ├────────────────────────────────────────────────────────────────────┤ \\
// │ Copyright © 2013 Jim Heising (https://github.com/jheising)         │ \\
// │ Copyright © 2013 Bug Labs, Inc. (http://buglabs.net)               │ \\
// ├────────────────────────────────────────────────────────────────────┤ \\
// │ Licensed under the MIT license.                                    │ \\
// └────────────────────────────────────────────────────────────────────┘ \\

(function () {
  
var thingspeakDatasource = function (settings, updateCallback) {
		var self = this;
		var updateTimer = null;
		var currentSettings = settings;
		
		
		function updateRefresh(refreshTime) {
			if (updateTimer) {
				clearInterval(updateTimer);
			}

			updateTimer = setInterval(function () {
				self.updateNow();
			}, refreshTime);
		}

		updateRefresh(currentSettings.refresh * 1000);
	
		this.updateNow = function () {
			
			var requestURL = currentSettings.url;

			$.ajax({
				url: requestURL,
				dataType: "html",
				success: function (data) {
					updateCallback(data);
				}
			});
		}
		this.onDispose = function () {
		clearInterval(updateTimer);
		updateTimer = null;
		}

		this.onSettingsChanged = function (newSettings) {
			currentSettings = newSettings;
			updateRefresh(currentSettings.refresh * 1000);
			self.updateNow();
		}
		
		createRefreshTimer(currentSettings.refresh);
		
		
	};
	freeboard.loadDatasourcePlugin({
		"type_name": "thingspeak_iot",
		"display_name": "Thingspeak",
		"description": "This plugin enables to get Thingspeak graphs embedded in channels",
		"settings": [
			{
				"name": "url",
				"display_name": "URL",
				"description": 'Replace CHANNEL_ID with the ID of the channel, FIELD_ID with the ID of the field that you want to chart, and XXXXXXXXXXXXX with the read API key of the private channel',
				"type": "text",
				"default_value": "http://thingspeak.com/channels/CHANNEL_ID/charts/FIELD_ID?api_key=XXXXXXXXXXXXX",			
			  
			},
			{
				"name": "refresh",
				"display_name": "Refresh Every",
				"type": "number",
				"suffix": "seconds",
				"default_value": 5
			},
			
		],
		newInstance: function (settings, newInstanceCallback, updateCallback) {
			newInstanceCallback(new thingspeakDatasource(settings, updateCallback));
		}
	});

	
}());
	