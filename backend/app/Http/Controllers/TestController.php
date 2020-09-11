<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class TestController extends Controller
{
    public function testApi(Request $request){
        return view('testApi');
    }

    public function testApiReceivePost(Request $request){
        /*echo $request['user-id'];
        echo $request['camera-num'];
        dd($request->file('webcam'));*/
        dd($request);
    }
}
