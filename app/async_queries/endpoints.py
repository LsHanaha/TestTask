from fastapi import APIRouter, status

from typing import List

import asyncio
import requests
import functools

from app.schemas import links_schemas
from app.config import settings


router = APIRouter(
    prefix='/async-links',
    tags=['async-links'],
    responses={404: {"description": "Not found"}}
)


_JSON_SERVERS_HOST = settings.json_server_host
_ASYNC_WORKERS_COUNT = 5


servers_schema = [
    {'port': settings.json_server1_port,
     'data': {
        'first': ((1, 11), (31, 41)),
        'third': ((21, 31), (51, 61))
        }
     },
    {'port': settings.json_server2_port,
     'data': {
        'second': ((11, 21), (41, 51))
        }
     }
]


async def make_async_request(url: str, loop: asyncio.AbstractEventLoop, result: list):

    # Not so sure that I can use aiohttp (Not in list of tech stack), that's why run_in_executor again
    try:
        response = await loop.run_in_executor(None, functools.partial(requests.get, url=url, timeout=2))
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
        else:
            data = []
    # Handle any error from any source (for timeout only I would prefer requests.Timeout)
    except Exception:
        data = []

    # In asyncio we have no problem with memory sharing, that's why a can use extend method
    # on common list object
    result.extend(data)


async def fill_async_queue():
    queue = asyncio.queues.Queue(maxsize=70)
    for json_server in servers_schema:
        port = json_server['port']
        for endpoint, id_range in json_server['data'].items():
            for range_ in id_range:
                for id_ in range(*range_):
                    url = f"{_JSON_SERVERS_HOST}:{port}/{endpoint}?id={id_}"
                    queue.put_nowait(url)
    return queue


async def worker(queue: asyncio.queues.Queue, loop: asyncio.AbstractEventLoop, result: list):
    while True:
        url = await queue.get()
        await make_async_request(url, loop, result)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()


async def make_request(queue: asyncio.queues.Queue, result: list):

    loop = asyncio.get_running_loop()
    tasks = []

    # Here I set some workers to make requests.
    for i in range(_ASYNC_WORKERS_COUNT):
        task = asyncio.create_task(worker(queue, loop, result))
        tasks.append(task)

    # Wait until the queue is fully processed.
    await queue.join()

    # Cancel worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)


def sort_list(data: List[dict]):
    result = sorted(data, key=lambda row: row['id'])
    return result


@router.get('/asyncio', response_model=List[links_schemas.Link])
async def using_asyncio():
    result = []
    url_queue = await fill_async_queue()

    await make_request(url_queue, result)

    return sort_list(result)
