ratingCruncherApp.controller('homeController', ['$scope', '$location', 'cityService', function($scope, $location, cityService) {
	$scope.city = cityService.city;
	$scope.$watch('city', function(){
		cityService.city = $scope.city;
	});
	$scope.submit = function() {
		$location.path("/forecast");
	};
}]);

ratingCruncherApp.controller('forecastController', ['$scope', '$resource', '$routeParams', 'cityService', function($scope, $resource, $routeParams, cityService) {
	$scope.city = cityService.city;
	$scope.numOpts = ['2', '3', '4', '5', '6', '7'];
	$scope.days = $routeParams.days || '2';
	$scope.weatherAPI = $resource("http://api.openweathermap.org/data/2.5/forecast/daily", {callback: "JSON_CALLBACK" }, { get: {method: "JSONP"}});
	
	$scope.weatherResult = $scope.weatherAPI.get({ q: $scope.city, cnt: $scope.days});
	$scope.convertToCelsius = function(degK) {
		return Math.round(degK - 272.15);
	};
	
	$scope.convertToDate = function(dt) {
		return new Date(dt * 1000);
	};
	
	$scope.isOptionActive = function(curVal, val){
		return (curVal == val)? 'active': '';
	}
}]);