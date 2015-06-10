// declare a module
var authAppModule = angular.module('authApp', ['ui.router'])
    .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider){
        $urlRouterProvider.otherwise('/');
        $stateProvider.state("home", {
            url: "/",
            templateUrl: "/static/js/index-default-message.html"
        });
    }]);
