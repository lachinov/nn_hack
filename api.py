# examples/server_simple.py
import aiohttp
from aiohttp import web
import json
import argparse
import cv2
import json
import numpy as np
import time
import io

import ImageProcessor
import utils


parser = argparse.ArgumentParser(description="Video Inference")
parser.add_argument("--ov_path", default="./", type=str, help="path to openvino models")

async def proctor_blocking(request):
    processor = request.app['processor']

    #if processor is None:
    #    print('Using cached response')
    #    frame = cv2.imread('image.jpg')
    #    _, byte_frame = cv2.imencode('.jpg',frame)

        # web.FileResponse()

    #    mpwriter = aiohttp.MultipartWriter(subtype='mixed')
    #    mpwriter.append_json({0: 'hello'}, {'name': 'response'})
    #    mpwriter.append(byte_frame.tostring(),
    #                   {'CONTENT-TYPE': 'image/jpeg',
    #                     'name': 'detection'})

    #    return web.Response(status=200, body=mpwriter)

        #respond here

    reader = await request.multipart()

    field = await reader.next()
    assert field.name == 'data' and field.headers[aiohttp.hdrs.CONTENT_TYPE] == 'application/json'
    data = await field.read(decode=True)
    data = json.loads(data.decode('utf8'))

    field = await reader.next()
    assert field.name == 'image' and field.headers[aiohttp.hdrs.CONTENT_TYPE] in ['image/jpeg', 'image/png']
    imageb = await field.read(decode=True)

    nparr = np.frombuffer(imageb, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    start = time.time()
    package = {'image': image}
    package = processor(package)
    end = time.time()
    inf_time = end - start

    print(1./inf_time, inf_time)

    frame = utils.render_gui(package, inf_time)

    _, byte_frame = cv2.imencode('.jpg',frame)

    cv2.imwrite('image.jpg', frame)

    #web.FileResponse()

    mpwriter = aiohttp.MultipartWriter(subtype='mixed')
    mpwriter.append_json({0:'hello'}, {'name' : 'response'})
    mpwriter.append(byte_frame.tostring(),
                    {'CONTENT-TYPE': 'image/jpeg',
                     'name' : 'detection'})

    return web.Response(status=200,body=mpwriter)

async def proctor_nonblocking(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


if __name__ == '__main__':
    opt = parser.parse_args()

    processor = None

    try:
        with open('model_config.json', 'r') as f:
            config = json.load(f)
        processor = ImageProcessor.FrameDetectionPipeline(opt.ov_path, config)
        processor.initialize()
    except Exception as e:
        print('ERROR: Couldn\'t load image processor')
        print(e)

    app = web.Application()
    app['processor'] = processor
    app.add_routes([web.post('/proctor', proctor_blocking),
                    web.post('/proctor_nonblocking', proctor_nonblocking)])
    web.run_app(app)
