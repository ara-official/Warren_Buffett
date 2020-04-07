import asyncio
import requests

from stock.creon.util import utils

async def get_page(loop, url):
    req = await loop.run_in_executor(None, requests.get, url)
    html = req.text
    print(html)
    return html

async def main(loop):
    urls = ["https://www.naver.com", "https://www.netflix.com/"]
    fts = [asyncio.ensure_future(get_page(loop, url)) for url in urls]
    r = await asyncio.gather(*fts)

def main_without_async():
    urls = ["https://www.naver.com", "https://www.netflix.com/"]
    for url in urls:
        req = requests.get(url)
        html = req.text
        print(html)

def test_async():
    __start_time = utils.Utils().현재_시간()
    print(__start_time)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    __end_time = utils.Utils().현재_시간()
    print(__end_time)

    print(__end_time-__start_time)

    print(loop)
    print(loop.close)

def test_sync():
    __start_time = utils.Utils().현재_시간()
    print(__start_time)
    main_without_async()
    __end_time = utils.Utils().현재_시간()
    print(__end_time)

    print(__end_time-__start_time)


if __name__ == "__main__":

    test_async() # 약 30초 소요
    test_sync() # 약 50초 소요
