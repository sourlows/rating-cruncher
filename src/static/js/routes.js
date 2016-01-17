ratingCruncherApp.config(function ($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: '/static/pages/home.html',
		controller: 'homeController'
	})
	.when('/forecast', {
		templateUrl: '/static/pages/forecast.html',
		controller: 'forecastController'
	})
	.when('/forecast/:days', {
		templateUrl: '/static/pages/forecast.html',
		controller: 'forecastController'
	});
});