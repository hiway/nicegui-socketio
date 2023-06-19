from typing import Any, Optional, Union

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from socketio import AsyncClient, AsyncNamespace, AsyncServer


class Agent(AsyncNamespace):
    def __init__(
        self,
        name: str,
        sio: Union[AsyncServer, AsyncClient, None] = None,
        namespace: str = "/agent",
    ):
        super().__init__(namespace)
        self.name = name
        if sio:
            sio.register_namespace(self)
        self.sio = sio or AsyncClient()
        self._ng_socket_path = "/_nicegui_ws/socket.io"
        self._event_handlers = {}
        self._scheduler = None
        self._scheduled_coros = {}

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

    async def emit(self, name: str, data: Any):
        await self.sio.emit(
            "frame",
            {
                "kind": "event",
                "name": name,
                "data": data,
            },
            namespace=self.namespace,
        )

    async def connect(self, url: str):
        if isinstance(self.sio, AsyncClient):
            await self.sio.connect(
                url, namespaces=[self.namespace], socketio_path=self._ng_socket_path
            )
        else:
            raise RuntimeError("Server Agent cannot connect.")

    async def disconnect(self):
        if isinstance(self.sio, AsyncClient):
            await self.sio.disconnect()
        else:
            raise RuntimeError("Server Agent cannot disconnect.")

    def on_interval(
        self,
        seconds: Optional[float] = None,
        minutes: Optional[float] = None,
        hours: Optional[float] = None,
    ):
        kwargs = {}
        if seconds is not None:
            kwargs["seconds"] = seconds
        if minutes is not None:
            kwargs["minutes"] = minutes
        if hours is not None:
            kwargs["hours"] = hours

        def wrapper(coro):
            self._scheduled_coros[coro] = kwargs
            return coro

        return wrapper

    async def start(self):
        self._scheduler = AsyncIOScheduler()
        for coro, kwargs in self._scheduled_coros.items():
            self._scheduler.add_job(coro, "interval", **kwargs)
        self._scheduler.start()

    async def stop(self):
        if self._scheduler:
            self._scheduler.shutdown()
