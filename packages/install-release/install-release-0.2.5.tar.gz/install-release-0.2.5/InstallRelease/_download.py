"""
A rudimentary URL downloader (like wget or curl) to demonstrate Rich progress bars.
"""

import os.path
import sys
from concurrent.futures import ThreadPoolExecutor
import signal
from functools import partial
from threading import Event
from urllib.request import urlopen

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from InstallRelease.utils import logger

progress = Progress(
    TextColumn("[bold blue]Downloading > ", justify="right"),
    BarColumn(bar_width=60),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)


done_event = Event()


def handle_sigint(signum, frame):
    done_event.set()


signal.signal(signal.SIGINT, handle_sigint)


def copy_url(task_id: TaskID, url: str, path: str) -> None:
    """Copy data from a url to a local file."""
    logger.debug(f"Requesting: {url}")
    response = urlopen(url)
    # This will break if the response doesn't contain content length
    progress.update(task_id, total=int(response.info()["Content-length"]))
    with open(path, "wb") as dest_file:
        progress.start_task(task_id)
        for data in iter(partial(response.read, 32768), b""):
            dest_file.write(data)
            progress.update(task_id, advance=len(data))
            if done_event.is_set():
                return
    logger.info(f"Downloaded: {path}")


def download(url: str, at: str):
    """Download multiple files to the given directory."""

    if not os.path.exists(at):
        os.makedirs(at)

    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            filename = url.split("/")[-1]
            dest_path = os.path.join(at, filename)
            task_id = progress.add_task("download", filename=filename, start=False)
            pool.submit(copy_url, task_id, url, dest_path)

            return f"{at}/{filename}"
