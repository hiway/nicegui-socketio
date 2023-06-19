import asyncio
import random

from socketio.exceptions import BadNamespaceError

from agent import Agent

progress = 0
agent = Agent(name="hello")


@agent.on_interval(seconds=2)
async def timed_job():
    global progress
    try:
        await agent.emit("progress-too", progress / 100)
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
    try:
        await asyncio.sleep(3)
        await agent.connect("ws://localhost:8080")
        await agent.start()
        while True:
            await asyncio.sleep(1)
    except asyncio.exceptions.CancelledError:
        print("\nStopping...")
    finally:
        await agent.stop()
        await agent.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
