<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateUsersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->timestamp('email_verified_at')->nullable();
            $table->string('password');
            $table->rememberToken();
            $table->timestamps();

            $table->boolean('is_teacher')->default(false)->nullable();
            $table->string('fio')->nullable();
            $table->string('description')->nullable();
            $table->string('token')->nullable();
            $table->string('camera_2_token')->nullable();
            $table->integer('room_id')->nullable();
            $table->boolean('connected')->default(false)->nullable();
            $table->boolean('is_exam_started')->default(false)->nullable();
            $table->boolean('is_user_banned')->default(false)->nullable();
            $table->text('view_map')->nullable();
            $table->integer('penalty')->default(0)->nullable();


        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('users');
    }
}
