var gulp = require('gulp');
var less = require('gulp-less');
var minifyCSS = require('gulp-minify-css');

// Compiles LESS > CSS
gulp.task('build-less', function(){
    return gulp.src('./src/static/css/less/styles.less')
        .pipe(less())
        .pipe(minifyCSS({advanced: true, keepSpecialComments: 0}))
        .pipe(gulp.dest('./src/static/css'));
});