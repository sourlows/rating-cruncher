ratingCruncherApp.service('cityService', function(){
	var cities =["Anaheim", "Chicago", "New York", "Tampa Bay"];
	this.city = cities[Math.floor(Math.random()*cities.length)];
});