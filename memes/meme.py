from pprint import pprint

import requests


async def get_random_meme() -> str:
    meme_api = "https://meme-api.com/gimme"
    response = requests.get(meme_api).json()
    meme = response.get("url")
    return meme
