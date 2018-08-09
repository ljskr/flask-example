// 引入gulp和gulp插件
var gulp = require('gulp'),
    rev = require('gulp-rev'),
    revCollector = require('gulp-rev-collector'),
    cleanCss = require('gulp-clean-css'),
    uglify = require('gulp-uglify'),
    promisedDel = require('promised-del');

// 定义css、js文件路径
var cssPath = './webapp/static/css/**/*.css',
    jsPath = './webapp/static/js/**/*.js';

// 监控文件变化
//gulp.task('watch', function () {
//    gulp.watch([jsPath, cssPath], ['default']);
//});

// 清除文件
gulp.task('clean', function(){
    return promisedDel([
            './webapp/static/dist',
            './webapp/templates_dist'
        ]);
});

// 处理 CSS 文件
gulp.task('revCss', function(){
    return gulp.src(cssPath)
            .pipe(rev())        // 生成md5 hash值，附在原文件名末尾
            .pipe(cleanCss())   // 压缩css
            .pipe(gulp.dest('./webapp/static/dist/css')) // 保存 css 文件
            .pipe(rev.manifest())  // 生成 rev-manifest.json 文件名对照映射
            .pipe(gulp.dest('./webapp/static/dist/rev/css')); // 保存 json 文件
});

// 处理 JS 文件
gulp.task('revJs', function(){
    return gulp.src(jsPath)
            .pipe(rev())        // 生成md5 hash值，附在原文件名末尾
            .pipe(uglify())     // 压缩js
            .pipe(gulp.dest('./webapp/static/dist/js')) // 保存 js 文件
            .pipe(rev.manifest())  // 生成 rev-manifest.json 文件名对照映射
            .pipe(gulp.dest('./webapp/static/dist/rev/js')); // 保存 json 文件
});

// 处理 Html 文件，更换css、js文件版本
gulp.task('revHtml', function () {
    return gulp.src(['./webapp/static/dist/rev/**/*.json', './webapp/templates/**/*.html']) // 前者是json映射文件，后者是html模板路径
            .pipe(revCollector({    // 文件名替换
                dirReplacements: {
                    'css': 'dist/css',
                    'js': 'dist/js'
                }
            }))
            .pipe(gulp.dest('./webapp/templates_dist'));  // 保存替换后的html文件
});

gulp.task('default',
    gulp.series(
        'clean',
        'revCss',
        'revJs',
        'revHtml',
        function(done) {
            done();
    })
);
