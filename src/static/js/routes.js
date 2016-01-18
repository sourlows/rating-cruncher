ratingCruncherApp.config(function ($routeProvider) {
	$routeProvider
	.when('/', {
		templateUrl: '/static/pages/home.html',
		controller: 'homeController'
	})
	.when('/explorer', {
		templateUrl: '/static/pages/explorer.html',
		controller: 'explorerController'
	})
	.when('/explorer/:days', {
		templateUrl: '/static/pages/explorer.html',
		controller: 'explorerController'
	});
});