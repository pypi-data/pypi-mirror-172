import asyncio

import aiohttp
from rich.console import Console
from arkitekt.apps.connected import App


async def check_fakts(endpoint_url: str):

    async with aiohttp.ClientSession(
        headers={"Content-Type": "application/json"}
    ) as session:
        # get json from endpoint
        async with session.get(endpoint_url) as resp:

            healthz_json = await resp.text()
            return healthz_json


async def check_app(app: App):

    async with app:
        check_futures = []
        check_keys = []

        for key, service in app:
            if hasattr(service, "healthz"):
                check_futures.append(service.healthz.check())
                check_keys.append(key)

        return dict(zip(check_keys, await asyncio.gather(*check_futures)))


async def check_fakts_loop(
    console: Console, endpoint_url: str, interval: int = 5, retries: int = 3
):

    while True:
        try:
            x = await check_fakts(endpoint_url)
            return x
            break

        except:
            if retries == 0:
                console.print(f"Failed to connect to {endpoint_url}")
                break
                raise

            else:
                console.print_exception()
                console.print("Retrying...")
                await asyncio.sleep(interval)
                retries -= 1
