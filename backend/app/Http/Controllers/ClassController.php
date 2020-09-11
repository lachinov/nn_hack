<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ClassController extends Controller
{
    public function getNewStudents(Request $request)
    {
        dd($request);
    }

    public function registerStudent(Request $request)
    {
        /*$student = Student::where('id', $request->id)->first();
        if(!$student){
            $student = new Student();
            $student->name = $request->name;
            $student->connected = false;
            $student->save();
        }*/
        return view('student')->with([]);
    }

    public function connectStudentToClass(Request $request)
    {
        /*$student = Student::where('id', $request->id)->first();
        if(!$student){return 500;}
        $student->token = $request['token'];
        $student->class_id = 1;*/
        return 1;
    }


}
