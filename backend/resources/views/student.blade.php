<!DOCTYPE html>
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
    </style>
</head>
<body class="blue-grey lighten-5">
<div id="app">
    <div class="container ">
        <div class="row">
            <div class="col s12">
                <div class="card white darken-1">
                    <div class="card-content">
                        <span class="card-title center">
                            Мой ID: <span id=myid ></span>
                        </span>
                    </div>
                    <div class="card-content">
                        <div class="row center">
                            <video id=myVideo muted="muted" width="100px" height="auto" style="position: absolute; margin-left: 5px; margin-top: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.5);" ></video>
                            <video id=remVideo width="400px" height="auto" style="box-shadow: 0 0 10px rgba(0,0,0,0.5);"></video>
                        </div>
                        <div id="my_camera" style="display: none;"></div>
                        <a class="waves-effect waves-light btn" onClick="take_snapshot()">Снимок камеры</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col s12">
                <iframe src="https://docs.google.com/forms/d/1dES0rZtBcJzxSWs8pDKbEo_vX2bdjr-FfXlmDHB-CCs/viewform?edit_requested=true" frameborder="1" style="
                    width: 100%;
                    height: 700px;
                "></iframe>
            </div>
        </div>
    </div>
</div>


<div id="results">Здесь будет снимок</div>

<br>


<script src="https://unpkg.com/peerjs@1.0.0/dist/peerjs.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/webcamjs/1.0.26/webcam.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
<script>
  var peer = new Peer();
  peer.on('open', function(peerID) {
    document.getElementById('myid').innerHTML=peerID;
  });

  var peercall;
  peer.on('call', (call)=>{
    // Answer the call, providing our mediaStream
    peercall=call;
    navigator.mediaDevices.getUserMedia ({ audio: true, video: { width:{ideal: 1280}, height:{ideal: 720} } }).then((mediaStream)=>{
      var video = document.getElementById('myVideo');
      peercall.answer(mediaStream); // отвечаем на звонок и передаем свой медиапоток собеседнику
      //peercall.on ('close', onCallClose); //можно обработать закрытие-обрыв звонка
      video.srcObject = mediaStream; //помещаем собственный медиапоток в объект видео (чтоб видеть себя)
      video.onloadedmetadata = (e)=>{//запускаем воспроизведение, когда объект загружен
        video.play();
      };

      setTimeout(()=>{
        //входящий стрим помещаем в объект видео для отображения
        document.getElementById('remVideo').srcObject = peercall.remoteStream;
        document.getElementById('remVideo').onloadedmetadata= (e)=>{
// и запускаем воспроизведение когда объект загружен
          document.getElementById('remVideo').play();
          console.log("2");
          Webcam.set({
            width: video.videoWidth,
            height: video.videoHeight,
            image_format: 'jpeg',
            jpeg_quality: 90
          });
          Webcam.attach( '#my_camera' );
        };
      },1500);

    }).catch(function(err) { console.log(err.name + ": " + err.message); });
  });


  function take_snapshot() {
    // take snapshot and get image data
    Webcam.snap( function(data_uri) {
      // display results in page
      document.getElementById('results').innerHTML =
        '<img src="'+data_uri+'"/>';
      Webcam.upload( data_uri, 'https://rtc-test.ml/webcamjs/demos/t.php', function(code, text) {
        console.log(code);
      } );
    } );
  }

</script>
</body>
</html>
