import asyncio
import random
import socketio
from socketio.exceptions import BadNamespaceError
from apscheduler.schedulers.asyncio import AsyncIOScheduler


sio = socketio.AsyncClient()
scheduler = AsyncIOScheduler()

progress = 0


@scheduler.scheduled_job("interval", seconds=2)
async def timed_job():
    global progress
    try:
        await sio.emit("frame", {
            "kind": "event",
            "name": "progress-too",
            "data": progress / 100,
        }, namespace="/agent")
        print(f"Sent: {progress}")
        if progress == 100:
            progress = 0
        elif progress > 100:
            progress = 100
        else:
            progress += random.randint(1, 10)
    except BadNamespaceError:
        print("BadNamespaceError")


async def main():
    scheduler.start()
    while True:
        # await asyncio.sleep(10)
        try:
            print("Connecting...")
            await sio.connect(
                "ws://localhost:8080",
                namespaces=["/agent"],
                socketio_path="/_nicegui_ws/socket.io",
            )
            scheduler.resume()
            await sio.wait()
        except asyncio.exceptions.CancelledError:
            print("\nStopping...")
            await sio.disconnect()
            break
        finally:
            print("Disconnecting...")
            scheduler.pause()
            await sio.disconnect()
            await asyncio.sleep(0.2)
    scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
