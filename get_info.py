import asyncio
import json
from ytmusicapi import YTMusic
import requests
from time import sleep

from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
)
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionPlaybackInfo as PlaybackInfo,
)

print("Connecting to YouTube Music...")
while True:
    try:
        yt = YTMusic()
    except requests.exceptions.ConnectionError:  # wait for internet connection
        print("No internet connection, retrying in 5 seconds...")
        sleep(5)
        continue
    else:
        break
print("Connected to YouTube Music")


def get_media_info():
    return asyncio.run(_get_media_info())


async def _get_media_info():
    sessions = await MediaManager.request_async()
    session = sessions.get_current_session()
    if not session:
        return None
    pinfo = session.get_playback_info()
    info = await session.try_get_media_properties_async()
    timeline = session.get_timeline_properties()
    # song_attr[0] != '_' ignores system attributes
    info_dict = {
        "artist": info.artist,
        "title": info.title,
        "genres": [x for x in info.genres],
        "playback_status": pinfo.playback_status,
        "playback_type": pinfo.playback_type,
        "end_time": timeline.end_time,
        "last_updated": timeline.last_updated_time,
        "max_seek": timeline.max_seek_time,
        "min_seek": timeline.min_seek_time,
        "position": timeline.position,
        "start_time": timeline.start_time,
    }
    return info_dict


def populate_yt(
    info_dict,
):  # populate info_dict with yt info  so that we don't spam the yt api. and only call it when we need to
    try:
        search = yt.search(
            f'{info_dict["title"]} {info_dict["artist"]}', filter="songs", limit=1
        )
    except Exception as e:
        search = None
    thumbnail = ""
    link = ""
    id = ""
    artists = []
    if search:
        if info_dict["title"] in search[0]["title"]:
            thumbnail = search[0]["thumbnails"][-1]["url"]
            link = f"https://music.youtube.com/watch?v={search[0]['videoId']}"
            id = search[0]["videoId"]
            artists = search[0]["artists"]
    info_dict["thumbnail"] = thumbnail
    info_dict["link"] = link
    info_dict["id"] = id
    info_dict["artists"] = artists
    return info_dict


if __name__ == "__main__":
    print(json.dumps(get_media_info(), indent=4, default=str))
