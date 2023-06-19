#!/usr/bin/env python3
from nicegui import Client, ui
from nicegui.globals import sio

from agent import Agent

progress = 0
progress_too = 0
agent = Agent(name="hello", sio=sio)


@ui.refreshable
def progress_bar():
    ui.linear_progress(progress, show_value=False)


@ui.refreshable
def progress_bar_too():
    ui.linear_progress(progress_too, show_value=False)


@ui.page("/")
async def main(client: Client):
    with ui.column().classes("absolute-center items-center"):
        ui.markdown("# Hello world!")
        progress_bar()
        ui.markdown("Progressing bars, please don't wait…").classes("pt-2")
        progress_bar_too()


@sio.on("progress", namespace="/test")  # type: ignore
async def on_progress(sid, value):
    global progress
    progress = value
    progress_bar.refresh()


@agent.on("progress-too")
async def on_progress_too(value):
    global progress_too
    progress_too = value
    progress_bar_too.refresh()


ui.run()
