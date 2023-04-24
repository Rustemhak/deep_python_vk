"""Script for asynchronous url paging"""

import sys
import asyncio
import aiohttp


def get_urls(file):
    """get urls"""
    with open(file, "r", encoding="utf-8") as filed:
        for line in filed.readlines():
            yield line


async def fetch_url(url, session, num):
    """fetch url"""
    async with session.get(url) as resp:
        data = await resp.read()

        return resp.status, len(data), num


async def worker(queue, session, num):
    """worker"""
    while True:
        url = await queue.get()
        try:
            res = await fetch_url(url, session, num)
            result.append(res)
        finally:
            queue.task_done()


async def fetch_batch_urls(queue, workers):
    """fetch batch urls"""
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(worker(queue, session, i)) for i in range(workers)]
        await queue.join()

        for task in tasks:
            task.cancel()


async def main(file, workers):
    """main"""
    urls_queue = asyncio.Queue()

    for url in get_urls(file):
        await urls_queue.put(url)

    await fetch_batch_urls(urls_queue, workers)


if __name__ == "__main__":
    # On Windows seems to be a problem with EventLoopPolicy:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = []
    if len(sys.argv) == 3:
        N = int(sys.argv[1])
        file_path = sys.argv[2]
        asyncio.run(main(file_path, N))
    elif len(sys.argv) == 4:
        N = int(sys.argv[2])
        file_path = sys.argv[3]
        asyncio.run(main(file_path, N))
    else:
        print(
            '"Incorrect running, example: python fetcher.py -c 10 urls.txt" \
            or "python fetcher.py 10 urls.txt"'
        )
