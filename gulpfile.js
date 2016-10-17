var gulp = require('gulp');

var sourcemaps = require('gulp-sourcemaps');

var babel = require('gulp-babel'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat');

var cleanCSS = require('gulp-clean-css'),
    sass = require('gulp-sass');


// var SASS_MIN_SRC = 'HackerPack/static/sass/*.sass',
//     SASS_MIN_DES = 'HackerPack/static/compressed/sass';

// gulp.task('minify-sass', function () {
//     return gulp.src(SASS_MIN_SRC)
//         .pipe(sourcemaps.init())
//         .pipe(sass({outputStyle: 'compressed'}))
//         .pipe(concat('main.min.css'))
//         .pipe(sourcemaps.write())
//         .pipe(gulp.dest(SASS_MIN_DES));
// });

var SCSS_MIN_SRC = 'HackerPack/static/scss/*.scss',
    SCSS_MIN_DES = 'HackerPack/static/compressed/scss';

gulp.task('minify-scss', function () {
    return gulp.src(SCSS_MIN_SRC)
        .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'compressed'}))
        .pipe(concat('main.min.css'))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(SCSS_MIN_DES));
});


// var CSS_MIN_SRC = 'HackerPack/static/css/main/*.css',
//     CSS_MIN_DES = 'HackerPack/static/compressed/css';
//
// gulp.task('minify-css', function () {
//     return gulp.src(CSS_MIN_SRC)
//         .pipe(sourcemaps.init())
//         .pipe(cleanCSS())
//         .pipe(concat('main.min.css'))
//         .pipe(sourcemaps.write())
//         .pipe(gulp.dest(CSS_MIN_DES));
// });

// var JS_MIN_SRC = 'HackerPack/static/js/*.js';
// var JS_MIN_DES = 'HackerPack/static/compressed/js';
//
//
// gulp.task('minify-js', function () {
//     return gulp.src([JS_MIN_SRC])
//         .pipe(jshint())
//         .pipe(jshint.reporter('default'))
//         .pipe(uglify({outSourceMap: true}))
//         .pipe(concat('main.min.js'))
//         .pipe(gulp.dest(JS_MIN_DES))
// });


//gulp.task('compile-es6-jsx', function () {
//    return gulp.src(JS_MIN_SRC)
//        .pipe(babel({
//            presets: ['es2015', 'stage-0', 'react']
//        }))
//        .pipe(gulp.dest(JS_MIN_DEST));
//});

gulp.task('watch', function () {
    gulp.watch(SCSS_MIN_SRC, ['minify-scss']);
    // gulp.watch(SASS_MIN_SRC, ['minify-sass']);
    // gulp.watch(CSS_MIN_SRC, ['minify-css']);
    // gulp.watch(JS_MIN_SRC, ['minify-js']);
});

gulp.task('default', ['watch']);