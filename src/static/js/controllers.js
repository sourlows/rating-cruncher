ratingCruncherApp.controller('homeController', function(){});

ratingCruncherApp.controller('explorerController', ['$scope', '$http', '$routeParams', 'cityService', function($scope, $http, $routeParams, cityService) {
    $scope.responseText = 'Press Submit to see the result';
    $scope.submit = function(){
        $scope.responseText = 'actual response';
    };
    var args = {
        leagueId: {
            name: 'league_id',
            displayName: 'League Id',
            required: true,
            type: 'string',
            disabled: false,
            default: 'LG-12345'
        },
        name: {
            name: 'name',
            displayName: 'Name',
            required: false,
            type: 'string',
            disabled: false,
            default: 'Mega League X'
        },
        ratingScheme: {
            name: 'rating_cheme',
            displayName: 'Rating Scheme',
            required: false,
            type: 'string',
            disabled: true,
            default: 'ELO'
        },
        description: {
            name: 'description',
            displayName: 'Description',
            required: false,
            type: 'string',
            default: 'A short explanation of your league.'
        },
        kSensitivity: {
            name: 'k_sensitivity',
            displayName: 'Sensitivity Factor (K)',
            required: false,
            type: 'integer',
            default: 15
        },
        decayRate: {
            name: 'k_factor_scaling',
            displayName: 'Sensitivity Decay Rate (K)',
            required: false,
            type: 'integer',
            default: 100
        }
    };
    $scope.endpoints = [
        {
            id: 0,
            url: '/league/',
            method: 'GET',
            description: 'Get all leagues',
            parameters: [
                args.leagueId
            ]
        },
        {
            id: 1,
            url: '/league/',
            method: 'POST',
            description: 'Create a  league',
            parameters: [
                args.leagueId,
                args.name,
                args.ratingScheme,
                args.description,
                args.kSensitivity,
                args.decayRate
            ]
        },
        {
            id: 2,
            url: '/league/:league_id',
            method: 'GET',
            description: 'Get a single league',
            parameters: [
                args.leagueId
            ]
        },
        {
            id: 3,
            url: '/league/:league_id',
            method: 'PUT',
            description: 'Update a single league',
            parameters: [
                args.leagueId,
                args.name,
                args.ratingScheme,
                args.description
            ]
        },
        {
            id: 4,
            url: '/league/:league_id',
            method: 'DELETE',
            description: 'Delete a single league',
            parameters: [
                args.leagueId
            ]
        }
    ];
    $scope.selectedEndpointId = null;
    $scope.getSelectedEndpoint = function(){
        if ($scope.selectedEndpointId === null){
            return null;
        }
        return $scope.endpoints.filter(function(endpoint){
            return $scope.selectedEndpointId === endpoint.id;
        })[0];
    };
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