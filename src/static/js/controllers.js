ratingCruncherApp.controller('homeController', function(){});

ratingCruncherApp.controller('explorerController', ['$scope', '$http', '$routeParams', 'cityService', function($scope, $http, $routeParams, cityService) {
    $scope.responseText = 'Press Submit to see the result';
    var args = {
        leagueId: {
            name: 'league_id',
            displayName: 'League Id',
            required: true,
            type: 'string',
            disabled: false,
            placeholder: 'LG-12345'
        },
        name: {
            name: 'name',
            displayName: 'Name',
            required: false,
            type: 'string',
            disabled: false,
            placeholder: 'Mega League X'
        },
        ratingScheme: {
            name: 'rating_scheme',
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
            placeholder: 'A short explanation of your league.'
        },
        kSensitivity: {
            name: 'k_sensitivity',
            displayName: 'Sensitivity Factor (K)',
            required: false,
            type: 'integer',
            placeholder: 15
        },
        decayRate: {
            name: 'k_factor_scaling',
            displayName: 'Sensitivity Decay Rate (K)',
            required: false,
            type: 'integer',
            placeholder: 100
        }
    };
    $scope.endpoints = [
        {
            id: 0,
            url: '/api/league/',
            method: 'GET',
            description: 'Get all leagues',
            parameters: [],
            route_parameters: []
        },
        {
            id: 1,
            url: '/api/league/',
            method: 'POST',
            description: 'Create a  league',
            parameters: [
                args.name,
                args.ratingScheme,
                args.description,
                args.kSensitivity,
                args.decayRate
            ],
            route_parameters: []
        },
        {
            id: 2,
            url: '/api/league/:league_id',
            method: 'GET',
            description: 'Get a single league',
            parameters: [
                args.leagueId
            ],
            route_parameters: [':league_id']
        },
        {
            id: 3,
            url: '/api/league/:league_id',
            method: 'PUT',
            description: 'Update a single league',
            parameters: [
                args.leagueId,
                args.name,
                args.ratingScheme,
                args.description
            ],
            route_parameters: [':league_id']
        },
        {
            id: 4,
            url: '/api/league/:league_id',
            method: 'DELETE',
            description: 'Delete a single league',
            parameters: [
                args.leagueId
            ],
            route_parameters: [':league_id']
        }
    ];
    $scope.selectedEndpointId = null;
    $scope.selectedEndpoint = {};
    $scope.form = null;

    $scope.credentials = btoa("124410202153178202201:fd8105ed212040faae963b7075372115");

    $scope.submit = function(){
        var submission = $scope.form;

        // replace tokens in url with form values
        var url = $scope.selectedEndpoint.url;
        $scope.selectedEndpoint.route_parameters.forEach(function(route_param){
            url = url.replace(route_param, submission[route_param.split(":").pop()]);
            delete submission[route_param.split(":").pop()];
        });


        $http({
            method: $scope.selectedEndpoint.method,
            url: url,
            data: submission,
            responseType: 'json',
            headers: {
                'Authorization': "Basic " + $scope.credentials
            }
        }).then(function(response) {
//          $scope.status = response.status;
          $scope.responseText = JSON.stringify(response.data, null, 2);;
        }, function(response) {
          $scope.responseText = response.data || "Request failed";
//          $scope.status = response.status;
        });
    };

    $scope.setSelectedEndpoint = function(){
        var newSelectedEndpoint = $scope.endpoints.filter(function(endpoint){
            return $scope.selectedEndpointId === endpoint.id;
        });
        $scope.form = {};
        $scope.selectedEndpoint = (newSelectedEndpoint.length > 0) ? newSelectedEndpoint[0]: {};

        // initialize default values for the form
        $scope.selectedEndpoint.parameters.forEach(function(param){
            $scope.form[param.name] = param.default;
        });
    };

    $scope.isSelected = function(endpointId){
        return $scope.selectedEndpointId === endpointId;
    };

    $scope.setSelected = function(endpointId){
        $scope.selectedEndpointId = endpointId;
        $scope.setSelectedEndpoint();
    };
}]);