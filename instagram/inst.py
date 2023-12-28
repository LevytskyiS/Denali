import asyncio
import os
import sys

sys.path.append(os.path.abspath("."))

from instagrapi import Client

from config.config import INSTAGRAM_LOGIN, INSTAGRAM_PASSWORD

cl = Client()
# cl.login(INSTAGRAM_LOGIN, INSTAGRAM_PASSWORD)


async def get_data_from_carousel(resources: list) -> list:
    result = []
    clean_links_to_photos = [
        l["thumbnail_url"] for l in resources if l["thumbnail_url"]
    ]
    clean_links_to_videos = [vid["video_url"] for vid in resources if vid["video_url"]]
    result += clean_links_to_photos
    result += clean_links_to_videos
    return result


async def get_media(url):
    result = []
    media_pk_from_url = cl.media_pk_from_url(url)
    media_info = cl.media_info(media_pk_from_url).model_dump()
    resources = media_info["resources"]

    if resources:
        photos_videos = await get_data_from_carousel(resources)
        result += photos_videos
        return result
    else:
        link_to_video = media_info["video_url"]

        if link_to_video:
            result.append(link_to_video)
            return result
        else:
            link_to_photo = media_info["thumbnail_url"]
            result.append(link_to_photo)
            return result


# print(asyncio.run(get_photo("https://www.instagram.com/p/C01cxyEqipf/")))
