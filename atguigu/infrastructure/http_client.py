from openai import AsyncClient


def init_http_client():
    global http_client
    http_client = AsyncClient()


async def close_http_client():
    await http_client.aclose()





