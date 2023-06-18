#!/usr/bin/env python3
from nicegui import Client, ui
from nicegui.globals import sio

progress = 0


@sio.on("progress", namespace="/test")  # type: ignore
async def on_progress(sid, value):
    global progress
    progress = value
    progress_bar.refresh()


@ui.refreshable
def progress_bar():
    ui.linear_progress(progress, show_value=False)


@ui.page("/")
async def main(client: Client):
    with ui.column().classes("absolute-center items-center"):
        ui.markdown("# Hello world!")
        progress_bar()
        ui.markdown("Progressing bars, please don't wait…")
        


ui.run()
