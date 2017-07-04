var gulp = require('gulp')
var pug = require('gulp-pug')
var concat = require('gulp-concat')
var less = require('gulp-less')
var csso = require('gulp-csso')
var del = require('del')

// Clean dirs
gulp.task('clean', function() {
  return del.sync(['app/static', 'app/templates']);
});

// jQuery
gulp.task('jquery', function(){
  return gulp.src('assets/bower_components/jquery/dist/jquery.min.js')
    .pipe(gulp.dest('static/js'));
});

// Bootstrap
gulp.task('bootstrap:css', function(){
  return gulp.src([
    'assets/bower_components/bootstrap/dist/css/bootstrap.min.css',
    'assets/bower_components/bootstrap/dist/css/bootstrap-theme.min.css'
  ])
    .pipe(gulp.dest('static/css'));
});

gulp.task('bootstrap:js', function(){
  return gulp.src('assets/bower_components/bootstrap/dist/js/bootstrap.min.js')
    .pipe(gulp.dest('static/js'));
});

gulp.task('bootstrap:fonts', function(){
  return gulp.src('assets/bower_components/bootstrap/dist/fonts/*')
    .pipe(gulp.dest('static/fonts'));
});

gulp.task('bootstrap', ['bootstrap:css', 'bootstrap:js', 'bootstrap:fonts']);

// Font awesome
gulp.task('fa:css', function(){
  return gulp.src('assets/bower_components/components-font-awesome/css/font-awesome.min.css')
    .pipe(gulp.dest('static/css'));
});

gulp.task('fa:fonts', function(){
  return gulp.src('assets/bower_components/components-font-awesome/fonts/*')
    .pipe(gulp.dest('static/fonts'));
});

gulp.task('fa', ['fa:css', 'fa:fonts']);

// Favicon
gulp.task('favicon', function(){
  return gulp.src('assets/favicon/*')
    .pipe(gulp.dest('static/favicon'));
});

// Prepare fonts
gulp.task('fonts', ['bootstrap:fonts', 'fa:fonts']);

// Prepare css
gulp.task('css', ['bootstrap:css', 'fa:css'], function(){
  return gulp.src('assets/css/*.less')
    .pipe(less())
    .pipe(csso())
    .pipe(gulp.dest('static/css'));
});

// Prepare pug
gulp.task('html', function(){
  return gulp.src([
    'assets/templates/**/*.pug',
    '!assets/templates/**/_*.pug'
  ])
    .pipe(pug({pretty: true}))
    // .pipe(on("error", console.log))
    .pipe(gulp.dest('templates'));
});

// Prepare js
gulp.task('js', ['jquery', 'bootstrap:js'], function(){
  return gulp.src('assets/js/**/*.js')
    .pipe(concat('index.js'))
    .pipe(gulp.dest('static/js'));
});

// Prepare images
gulp.task('images', function(){
  return gulp.src('assets/images/*')
    .pipe(gulp.dest('static/images'));
});

// Watch for changes
gulp.task('watch', ['fonts', 'css', 'html', 'js', 'images'], function() {
  gulp.watch('assets/css/*.less', ['css']);
  gulp.watch('assets/templates/**/*.pug', ['html']);
  gulp.watch('assets/js/**/*.js', ['js']);
  gulp.watch('assets/images/*', ['images']);
});

gulp.task('default', ['clean', 'favicon', 'fonts', 'html', 'css', 'js', 'images']);
