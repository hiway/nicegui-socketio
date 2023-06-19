import asyncio
import random


from agent import Agent

progress = 0
agent = Agent(name="hello")


@agent.on_interval(seconds=1)
async def timed_job():
    global progress
    try:
        if progress == 100:
            progress = 0
        elif progress > 100:
            progress = 100
        else:
            progress += random.randint(1, 10)
        progress = min(100, progress)
        print("Emitting progres: ", progress)
        await agent.emit("progress-too", progress / 100)
    except ConnectionError:
        print("ConnectionError")


if __name__ == "__main__":
    asyncio.run(agent.run("ws://localhost:8080"))
