<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Экзамен</title>

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

        <style>
            video{
                width: 100%;
            }
            .ava{
                max-width: 70px;
            }
            .ava-area{
                margin-bottom: 0px;
                padding-bottom: 15px;
                box-shadow: none;
            }
            .valign-wrapper{
                margin-bottom: 0px;
            }
            .video-wrapper{

            }
            .mini-video{
                margin: 10px;
                border-radius: 5px;
                box-shadow: 0 0 5px rgba(0,0,0,0.5);
            }
            .mini-video-header{
                margin: 0px;
            }

            .tabs .tab a {
                color: #29b6f6;
                /*Custom Text Color*/
            }

            .tabs .tab a:hover {
                color:#29b6f6;
                /*Custom Color On Hover*/
            }

            .tabs .tab a:focus.active {
                color:#b3e5fc;
                /*Custom Text Color While Active*/
                background-color: #e1f5fe;
                /*Custom Background Color While Active*/
            }

            .tabs .indicator {
                background-color:#0288d1;
                /*Custom Color Of Indicator*/
            }

            .tabs .tab a:hover, .tabs .tab a.active{
                color: #01579b;
            }

            .tabs .tab a:focus.active{
                color: #01579b;
            }

            .activity{
                padding-right: 10px;
            }

            .card-image.img
            {
                height:150px; !important
            }

            .material-icons.md1::before{
                content:"search";
            }

            .material-icons.md1:hover::before{
                content:"navigate_next";
            }

            .carousel-item{
                top: -20px !important;
            }

            .carousel{
                height: 210px;
            }

            .name{
                font-size: 125%;
            }

            svg{
                height: 100px;
            }
            circle{
                fill: #fff;
                opacity: .8;
            }

            .card-center{
                margin-bottom: 0px;
            }

        </style>
    </head>
    <body>
    <nav class="light-blue lighten-1" role="navigation">
        <div class="nav-wrapper container"><a href="#" class="brand-logo">Экзамен</a>
            <ul class="right hide-on-med-and-down">
                <li><a href="#">Настройки</a></li>
            </ul>

            <ul id="nav-mobile" class="sidenav">
                <li><a href="#">Navbar Link</a></li>
            </ul>
        </div>
    </nav>


    <div class="container">
        <div class="row">


            <div class="col s12">
                <div class="card">
                    <div class="card-panel grey lighten-5 z-depth-1 ava-area">
                        <div class="row valign-wrapper">
                            <div class="col ava">
                                <img src="https://materializecss.com/images/yuna.jpg" alt="" class="circle responsive-img"> <!-- notice the "circle" class -->
                            </div>
                            <div class="col">
          <span class="black-text">
              <span class="name">Иванов Петр</span><br>
              Ученик 11 "Б" класса школы №1
          </span>
                            </div>
                        </div>
                    </div>
                    <div class="row card-center">
                        <div class="col s4 video-wrapper">
                            <div class="row center mini-video-header">Фронтальная камера</div>
                            <video preload="none" autoplay loop muted class="mini-video">
                                <source src="https://rtc-test.ml/videos/t1.mp4" type="video/mp4">
                            </video>
                        </div>
                        <div class="col s4 video-wrapper">
                            <div class="row center mini-video-header">Боковая камера</div>
                            <video preload="none" autoplay loop muted class="mini-video">
                                <source src="https://rtc-test.ml/videos/t1.mp4" type="video/mp4">
                            </video>
                        </div>
                        <div class="col s4">
                            <div class="activity">
                                <div class="row center mini-video-header">Активность</div>
                                концентрация: 70%
                                <div class="progress">
                                    <div class="determinate" style="width: 70%"></div>
                                </div>
                                волнение: 40%
                                <div class="progress">
                                    <div class="determinate" style="width: 40%"></div>
                                </div>
                                нарушения: 2
                                <div class="progress progress-red red lighten-4">
                                    <div class="determinate red" style="width: 10%"></div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="card-tabs">
                        <ul class="tabs tabs-fixed-width">
                            <li class="tab"><a href="#c1-test4">Нарушения</a></li>
                            <li class="tab"><a href="#c1-test5">Карта взгляда</a></li>
                            <li class="tab"><a href="#c1-test6">Активность</a></li>
                        </ul>
                    </div>
                    <div class="card-content grey lighten-4">
                        <div id="c1-test4">
                            <div class="carousel">
                                <div class="carousel-item">
                                    <div class="card sticky-action">
                                        <div class="card-image ">
                                            <img src="https://images.pexels.com/photos/160933/girl-rabbit-friendship-love-160933.jpeg?h=350&auto=compress&cs=tinysrgb">
                                        </div>
                                        <div class="card-content">
                                            <p>Использование телефона</p>
                                        </div>
                                    </div>
                                </div>

                                <div class="carousel-item">
                                    <div class="card sticky-action">
                                        <div class="card-image ">
                                            <img src="https://images.pexels.com/photos/160933/girl-rabbit-friendship-love-160933.jpeg?h=350&auto=compress&cs=tinysrgb">
                                        </div>
                                        <div class="card-content">
                                            <p>Помощь постороннего</p>
                                        </div>
                                    </div>
                                </div>

                                <div class="carousel-item">
                                    <div class="card sticky-action">
                                        <div class="card-image ">
                                            <img src="https://images.pexels.com/photos/160933/girl-rabbit-friendship-love-160933.jpeg?h=350&auto=compress&cs=tinysrgb">
                                        </div>
                                        <div class="card-content">
                                            <p>Уход с рабочего места</p>
                                        </div>
                                    </div>
                                </div>



                            </div>
                        </div>
                        <div id="c1-test5" class="center">

                            <svg viewBox="0 0 400 100" xmlns="http://www.w3.org/2000/svg">
                                <defs>
                                    <circle
                                            id = "spot"
                                            cx = "0"
                                            cy = "0"
                                            r = "10"/>

                                    <filter id="heatmapFilter">
                                        <feGaussianBlur
                                                stdDeviation="5" />

                                        <feColorMatrix
                                                color-interpolation-filters="sRGB"
                                                type="matrix"
                                                values= "0 0 0 0 1
               0 0 0 -1 1
               0 0 0 0 0
               0 0 0 1.2 0.01"/>
                                    </filter>
                                </defs>

                                <g
                                        id = "heatmap"
                                        filter="url(#heatmapFilter)">
                                    <use transform = "translate(100, 30)" xlink:href = "#spot"/>
                                    <use transform = "translate(200, 50)" xlink:href = "#spot"/>
                                    <use transform = "translate(205, 70)" xlink:href = "#spot"/>
                                    <use transform = "translate(290, 80)" xlink:href = "#spot"/>
                                    <use transform = "translate(310, 45)" xlink:href = "#spot"/>
                                    <use transform = "translate(390, 30)" xlink:href = "#spot"/>
                                    <use
                                            transform = "translate(50, 10)"
                                            xlink:href = "#spot"/>
                                    <use
                                            transform = "translate(50, 10)"
                                            xlink:href = "#spot"/>
                                    <use
                                            transform = "translate(45, 40)"
                                            xlink:href = "#spot"/>
                                    <use
                                            transform = "translate(60, 20)"
                                            xlink:href = "#spot"/>
                                    <use
                                            transform = "translate(90, 90)"
                                            xlink:href = "#spot"/>

                                </g>
                            </svg>

                        </div>
                        <div id="c1-test6">

                            <canvas id="c1-myChart" height="100"></canvas>


                        </div>
                    </div>
                </div>
            </div>





















        </div>
    </div>

    <!--  Scripts-->
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.1.3/Chart.js"></script>
    <script>


    function refrashTabs(){
      var el = document.querySelector('.tabs');
      var instance = M.Tabs.init(el, {});
    }

      $(document).ready(function(){
        $('.carousel').carousel({
          dist:0,
          shift:0,
          padding:20,

        });
      });
    refrashTabs()

      const colors = {
        green: {
          fill: '#e0eadf',
          stroke: '#5eb84d',
        },darkBlue: {
          fill: '#92bed2',
          stroke: '#3282bf',
        },
      };

      const unrest = [70, 40, 20, 25, 30, 32, 50];
      const concentration = [90, 85, 70, 50, 55, 60, 35];
      const xData = ['8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00'];

      var ctx = document.getElementById("c1-myChart").getContext("2d");
      const myChart1 = new Chart(ctx, {
        type: 'line',
        data: {
          labels: xData,
          datasets: [{
            label: "концентрация",
            fill: true,
            backgroundColor: 'rgba(41, 186, 243, 0.2)',
            borderColor: 'rgba(41, 186, 243)',
            borderCapStyle: 'butt',
            data: concentration,
          }, {
            label: "Волнение",
            fill: true,
            backgroundColor: 'rgba(38, 200, 154, 0.2)',
            borderColor: 'rgba(38, 200, 154)',
            data: unrest,
          }]
        },
        options: {
          responsive: true,
          // Can't just just `stacked: true` like the docs say
          scales: {
            yAxes: [{
              stacked: false,
            }]
          },
          animation: {
            duration: 750,
          },
        }
      });


    </script>
    </body>


</html>
