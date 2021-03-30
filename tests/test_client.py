import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8086/', data=b'Hello', timeout=2) as resp:
            print(resp.status)
            print(await resp.text())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())