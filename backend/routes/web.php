<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/student', function () {
    return view('student');
});

Route::post('/student-connect-to-class', 'ClassController@connectStudentToClass');

Route::post('/student', 'ClassController@registerStudent');

Route::group(['middleware' => 'auth'], function(){
    Route::get('/teacher', function () {
        return view('teacher');
    });
    Route::post('/teacher-ajax', 'ClassController@getNewStudents');
});

Route::get('/conference', function () {
    return view('videoConference');
});

Route::get('/test-api', 'TestController@testApi');

Route::post('/test-api-receive-post', 'TestController@testApiReceivePost');

Auth::routes();

/* teacher.blade.php
Route::group(['middleware' => 'auth'], function(){
    Route::get('video_chat', 'VideoChatController@index');
    Route::post('auth/video_chat', 'VideoChatController@auth');
    Route::get('video-conference', function () {
        return view('videoConference');
    });

});

Route::get('/hi', function () {
    return 'hi';
});

Route::get('/picture-from-camera', function () {
    return view('pictureFromCamera');
});

Route::get('/', function () {
    return view('welcome');
});

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
*/
