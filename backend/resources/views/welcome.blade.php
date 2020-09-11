<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <title>Войдите на экзамен</title>
    <style>
        .center-card {
            margin: 0px;
            padding:0px;
            float: left;
            width:100%;
            position:absolute;
            top: 50%;
            transform: translateY(-50%) translateX(-50%);
            left:50%;
        }

        .bordered{
            border-left: 1px solid;
            border-color: #dadddf;
        }

        .btn {
            margin-left: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body class="blue-grey lighten-5">
    <div id="app">
        <div class="container">
            <div class="row center-card">
                <div class="col s8 offset-s2 xl6 offset-xl3 valign-wrapper">
                    <div class="card white darken-1">
                        <div class="row">
                            <div class="col s12">
                                <div class="card-content teal white-text">
                                    <span class="card-title center">Войдите на экзамен</span>
                                </div>
                            </div>

                        </div>
                        <div class="row">
                            <div class="col s12 m6">
                                <div class="card-content white">
                                    <span class="card-title">Как студент</span>
                                    <span class="card-content">
                                        <form class="col s12" action="student" method="post" ref="studentForm">
                                        <div class="row">
                                            <div class="input-field col s12">
                                                <i class="material-icons prefix">account_circle</i>
                                                <input name="name" id="icon_prefix" type="text" class="validate" v-model="name">
                                                <label for="icon_prefix">Имя Отчество</label>
                                            </div>
                                            @csrf
                                            <input name="id" v-model="studentId" hidden>
                                            <a class="waves-effect waves-light btn" @click="studentIn()">Войти</a>
                                            <!--<button class="btn waves-effect waves-light" type="submit" name="action">
                                                Войти
                                            </button>-->
                                        </div>
                                    </form>
                                    </span>
                                </div>
                            </div>
                            <div class="col s12 m6 bordered">
                                <div class="card-content">
                                    <span class="card-title">Как преподаватель</span>
                                    <span class="card-content">
                                        <form class="col s12" action="teacher" method="post" ref="teacherForm">
                                        <div class="row">
                                            <div class="input-field col s12">
                                                <i class="material-icons prefix">account_circle</i>
                                                <input id="email" type="text" class="validate" v-model="email">
                                                <label for="email">email</label>
                                            </div>

                                            <div class="input-field col s12">
                                                <i class="material-icons prefix">vpn_key</i>
                                                <input id="icon_telephone" type="password" class="validate" v-model="pass">
                                                <label for="icon_telephone">Пароль</label>
                                            </div>
                                            @csrf
                                            <a class="waves-effect waves-light btn" href="https://fillin-ai.ru/p2p/teacher2.html">Войти</a>

                                        </div>
                                    </form>
                                    </span>
                                </div>
                            </div>
                            <span class="card-content center red-text">{%message%}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
    <script>
      let app = new Vue({
        el: '#app',
        delimiters: ['{%', '%}'],
        data: {
          name: '',
          email: '',
          pass: '',
          studentId: '',
          csrf: '',
          message: '',
        },
        methods: {
          studentIn(){
            this.message = '';
            if(!this.name){
              this.message = 'Введите Ваше имя и отчество';
              return 0;
            }
            localStorage.setItem('name', this.name);
            this.$refs.studentForm.submit()
          },
        },
        created(){
          this.csrf = document.querySelector('meta[name="csrf-token"]').content;
          if(localStorage.hasOwnProperty('studentId')){this.studentId = localStorage.getItem('studentId');}
        },
      })
    </script>
</body>
</html>
