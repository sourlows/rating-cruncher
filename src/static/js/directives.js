ratingCruncherApp.directive("weatherReport", function() {
	return { 
		restrict: 'E',
		templateUrl: 'static/directives/weatherReport.html',
		replace: true,
		scope: {
			weatherDay: "=",
			convertToStandard: "&",
			convertToDate: "&",
			dateFormat: "@"
		}
	}
});

ratingCruncherApp.directive("numericalOption", function() {
	return { 
		restrict: 'E',
		templateUrl: 'static/directives/numericalOption.html',
		replace: true,
		scope: {
			val: "@",
			curVal: "@",
			applyActive: "&"
		}
	}
});