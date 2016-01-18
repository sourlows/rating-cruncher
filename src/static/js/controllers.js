ratingCruncherApp.controller('homeController', function(){});

ratingCruncherApp.controller('explorerController', ['$scope', '$http', '$routeParams', 'cityService', function($scope, $http, $routeParams, cityService) {
    $scope.responseText = 'Press Submit to see the result';
    $scope.submit = function(){
        $scope.responseText = 'actual response';
    };
    $scope.endpoints = [
        {
            id: 0,
            url: '/league/',
            route_parameters: [
                'League Id'
            ]
        }
    ];
    debugger;
//	$scope.city = cityService.city;
//	$scope.numOpts = ['2', '3', '4', '5', '6', '7'];
//	$scope.days = $routeParams.days || '2';
//	$scope.weatherAPI = $resource("http://api.openweathermap.org/data/2.5/forecast/daily", {callback: "JSON_CALLBACK" }, { get: {method: "JSONP"}});
	
//	$scope.weatherResult = $scope.weatherAPI.get({ q: $scope.city, cnt: $scope.days});
//	$scope.convertToCelsius = function(degK) {
//		return Math.round(degK - 272.15);
//	};
//
//	$scope.convertToDate = function(dt) {
//		return new Date(dt * 1000);
//	};
//
//	$scope.isOptionActive = function(curVal, val){
//		return (curVal == val)? 'active': '';
//	}
}]);