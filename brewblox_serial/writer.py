"""
Writing serial commands
"""


from aiohttp import web
from brewblox_service import brewblox_logger, features

from brewblox_serial import communication

LOGGER = brewblox_logger(__name__)
routes = web.RouteTableDef()


def setup(app: web.Application):
    features.add(app, Writer(app))
    app.router.add_routes(routes)


def get_writer(app: web.Application):
    return features.get(app, Writer)


class Writer(features.ServiceFeature):

    def __init__(self, app: web.Application):
        super().__init__(app)

        self._conduit: communication.SparkConduit = None

    def __str__(self):
        return f'<{type(self).__name__} for {self._conduit} at {hex(id(self))}>'

    async def _on_event(self, conduit, msg: str):
        LOGGER.info(f'Received Event: "{msg}"')

    async def _on_data(self, conduit, msg: str):
        LOGGER.info(f'Received Data: "{msg}"')

    async def startup(self, app: web.Application):
        await self.shutdown()
        self._conduit = communication.get_conduit(app)
        self._conduit.data_callbacks.add(self._on_data)
        self._conduit.event_callbacks.add(self._on_event)

    async def shutdown(self, *_):
        if self._conduit:
            self._conduit.data_callbacks.discard(self._on_data)
            self._conduit.event_callbacks.discard(self._on_event)
            self._conduit = None

    async def write(self, msg: str):
        LOGGER.info(f'Writing: "{msg}"')
        return await self._conduit.write(msg)


@routes.post('/write')
async def object_create(request: web.Request) -> web.Response:
    """
    ---
    summary: Write to serial port
    tags:
    - Serial
    operationId: serial.write
    produces:
    - application/json
    parameters:
    -
        in: body
        name: body
        description: object
        required: true
        schema:
            type: object
            properties:
                message:
                    type: string
                    example: 0x00
    """
    request_args = await request.json()
    msg = request_args['message']
    written = await get_writer(request.app).write(msg)

    return web.json_response({'written': written})
