# nn_hack

Репозиторий ПО для прокторинга экзаменов

Вебсервис получает POST запрос вида:







## Докеры


Запустить докер с вебсервисом, чтобы он ловил POST запросы снаружи на 5000 порт (OpenVINO с моделями уже упакованы внутрь):

```bash
docker run -it fenixfly/vinoserver -p 5000:8080
```

Запустить его в виде демона: 

```bash
docker run -d fenixfly/vinoserver -p 5000:8080
```


### Докер с OpenVINO - fenixfly/vinodock

Сборка: положить архив с OpenVINO `l_openvino_toolkit_p_2020.4.287.tgz` в папку `docker/openvino` и запустить сборку
 

```bash
docker build -t fenixfly/vinodock -f dockers/openvino/Dockerfile dockers/openvino 
```

Запуск (на всякий случай)

```bash
docker run -it fenixfly/vinodock bash
```

### Докер с вебсервисом - fenixfly/vinodock

Сборка:
 
```bash
docker build -t fenixfly/vinoserver -f dockers/webserver/Dockerfile . 
```

Запуск:

```bash
docker run -it fenixfly/vinoserver -p 5000:8080  
```


