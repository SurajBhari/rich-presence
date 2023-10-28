import asyncio
import json
from ytmusicapi import YTMusic


from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackInfo  as PlaybackInfo



yt = YTMusic()


def get_media_info():
    return asyncio.run(_get_media_info())

async def _get_media_info():
    sessions = await MediaManager.request_async()
    session = sessions.get_current_session()
    if not session:
        return None
    if session:  # there needs to be a media session running
        pinfo = session.get_playback_info()
        info = await session.try_get_media_properties_async()
        timeline = session.get_timeline_properties()
        # song_attr[0] != '_' ignores system attributes
        info_dict = {
            "artist": info.artist,
            "title": info.title,
            "genres": info.genres,
            "playback_status": pinfo.playback_status,
            "duration": pinfo.playback_type,
            "end_time": timeline.end_time,
            "last_updated": timeline.last_updated_time,
            "max_seek": timeline.max_seek_time,
            "min_seek": timeline.min_seek_time,
            "position": timeline.position,
            "start_time": timeline.start_time
        }
        try:
            search = yt.search(f'{info.title} {info.artist}', filter="songs", limit=1)
        except Exception as e:
            search = None
        thumbnail = ""
        link = ""
        if search:
            if info.title in search[0]['title']:
                thumbnail = search[0]['thumbnails'][-1]['url']
                link = f"https://music.youtube.com/watch?v={search[0]['videoId']}"
        info_dict['thumbnail'] = thumbnail
        info_dict['link'] = link
        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])
        return info_dict
    raise Exception('TARGET_PROGRAM is not the current media session')


if __name__ == '__main__':
    print(json.dumps(get_media_info(), indent=4, sort_keys=True, default=str))
    
