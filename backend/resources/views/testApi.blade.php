<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
тест api
<div id="app">
    <form :action="to" method="post">
        куда<input type="text" v-model="to"><br>
        user-id<input type="text" name="user-id"><br>
        camera-num<input type="text" name="camera-num"><br>
        picture<input name="picture" type="file">

        <button type="submit">отправить</button>
    </form>
</div>

<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
<script>
  let app = new Vue({
      el: '#app',
      delimiters: ['{%', '%}'],
      data: {
        to: 'https://fillin-ai.ru/test-api-receive-post',
      }
    });
</script>
</body>
</html>
