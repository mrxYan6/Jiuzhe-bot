import httpx
import asyncio

async def get_html(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        'Connection': 'close'
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url=url, headers=headers)
        
    return r.text



async def get_json(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        'Connection': 'close'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=headers)
        json_data = response.json()
        # await asyncio.sleep(5)
        return json_data
    except:
        return -1