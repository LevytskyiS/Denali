import json
from pprint import pprint

import requests

memes_json = "data/memes.json"


async def get_random_meme() -> str:
    meme_api = "https://meme-api.com/gimme"
    response = requests.get(meme_api).json()
    meme = response.get("url")

    # It doesn't make any sense to check if the file us unique,
    # because there are something for about 60 memes

    # try:
    #     with open(memes_json, "r", encoding="utf-8") as fh:
    #         memes = json.load(fh)
    # except FileNotFoundError as e:
    #     memes = {"meme": []}
    #     with open(memes_json, "w", encoding="utf-8") as fh:
    #         json.dump(meme, fh, indent=4)

    # urls = memes.get("meme")
    # if meme not in urls:
    #     urls.append(meme)
    #     memes["meme"] = urls

    #     with open(memes_json, "w", encoding="utf-8") as fh:
    #         json.dump(memes, fh, indent=4)

    #     return meme

    # return await get_random_meme()
    return meme
