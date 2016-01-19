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
            method: 'GET',
            description: 'Get all leagues',
            route_parameters: [],
            arguments: []
        },
        {
            id: 1,
            url: '/league/',
            method: 'POST',
            description: 'Create a  league',
            route_parameters: [
                'League Id'
            ],
            arguments: [
                'Name',
                'Rating Scheme',
                'Description',
                'Sensitivity Factor (K)',
                'Decay Rate of K'
            ]
        },
        {
            id: 2,
            url: '/league/:league_id',
            method: 'GET',
            description: 'Get a single league',
            route_parameters: [
                'League Id'
            ],
            arguments: []
        },
        {
            id: 3,
            url: '/league/:league_id',
            method: 'PUT',
            description: 'Update a single league',
            route_parameters: [
                'League Id'
            ],
            arguments: [
                'Name',
                'Rating Scheme',
                'Description'
            ]
        },
        {
            id: 4,
            url: '/league/:league_id',
            method: 'DELETE',
            description: 'Delete a single league',
            route_parameters: [
                'League Id'
            ],
            arguments: []
        }
    ];
    $scope.selectedEndpointId = null;
    $scope.isSelected = function(endpointId){
        return $scope.selectedEndpointId === endpointId;
    };
    $scope.setSelected = function(endpointId){
        $scope.selectedEndpointId = endpointId;
    };
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