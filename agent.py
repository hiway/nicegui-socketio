from typing import Any, Coroutine, Union
from socketio import AsyncServer, AsyncClient, AsyncNamespace


class Agent(AsyncNamespace):
    def __init__(self, name: str, sio: Union[AsyncServer, AsyncClient], namespace: str = "/agent"):
        self.name = name
        self.sio = sio # or AsyncClient()
        super().__init__(namespace)
        self._event_handlers = {}

    async def on_connect(self, sid, environ):
        print(f"NS Connected: {sid}")

    async def on_disconnect(self, sid):
        print(f"NS Disconnected: {sid}")

    async def on_frame(self, sid, frame):
        if frame["kind"] == "event" and frame["name"] in self._event_handlers:
            for handler in self._event_handlers[frame["name"]]:
                await handler(frame["data"])

    def on(self, name: str):
        def wrapper(coro):
            if name in self._event_handlers:
                self._event_handlers[name].append(coro)
            else:
                self._event_handlers[name] = [coro]
            return coro
        return wrapper
