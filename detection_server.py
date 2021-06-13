from aiohttp import web
import aiohttp
# from detection.detection_task import detect_cards
# from task_queue.celery import celery_app
from detection.recognition_task import recongition_task
from celery.result import AsyncResult
import asyncio
import codecs
import base64
import sys


class DetectionQueue:

    def __init__(self):
        pass

class DetectionHandler:

    def __init__(self):
        self._handler_routes = web.RouteTableDef()
        self._set_handlers()
    
    def _set_handlers(self):
        
        @self._handler_routes.post('/')
        async def handle_task(request:web.Request):
            try:
                data = await self._extract_data_from_request(request)                  
                async_res = recongition_task.apply_async((data,),serializer='pickle', time_limit=60)
                result = await self.wait_for_result(async_res)
            except asyncio.CancelledError as ex:
                print(ex)
                return web.HTTPInternalServerError()
            else:
                return web.json_response(result)
                # return web.Response(text="Hello you to")
    
    async def wait_for_result(self, result:AsyncResult):
        try:
            while not result.ready():
                await asyncio.sleep(1)
        except result.TimeoutError:
            print('Task timeout exceeded')
            raise
        except Exception:
            print('Internal task error')
            raise
        else:
            return result.get()

    async def _extract_data_from_request(self, request:web.Request) -> bytes:
        if request.content_type == 'multipart/form-data':
            image_reader = await request.multipart()
            parts = []
            while True:
                part = await image_reader.next()
                if part is None: break
                data = await self._recive_data_from_stream_reader(part)
                parts.append(data)
            return parts[-1]
        else:
            raise web.HTTPUnsupportedMediaType(reason='Type: ' \
                                            + request.content_type \
                                            + " is not supported")

    async def _recive_data_from_stream_reader(self, stream_reader):
        try:
            data = b""
            async for recived_data in stream_reader:
                data += recived_data
            return data    
        except aiohttp.StreamReader().exception():
            raise web.HTTPNoContent(reason='Can`t read content')

    def get_handler_routes(self) -> web.RouteTableDef:
        return self._handler_routes


class DetectionServer:

    def __init__(self, host='192.168.1.167', port=6451):
        self._host = host
        self._port = port
        self._det_handler = DetectionHandler()
        self._app = web.Application() 
        self._set_routes()
    
    def _set_routes(self):
        self._app.add_routes(self._det_handler.get_handler_routes())
    
    def run(self):
        web.run_app(self._app, host=self._host, port=self._port)



if __name__ == "__main__":
    detection_server = DetectionServer()
    detection_server.run()



