var gulp = require('gulp');
var less = require('gulp-less');

// Compiles LESS > CSS
gulp.task('build-less', function(){
    return gulp.src('./static/css/less/styles.less')
        .pipe(less())
        .pipe(gulp.dest('./static/css'));
});