import asyncio
import json


from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackInfo  as PlaybackInfo


def get_media_info():
    return asyncio.run(_get_media_info())

async def _get_media_info():
    sessions = await MediaManager.request_async()
    session = sessions.get_current_session()
    if not session:
        return None
    TARGET_ID = session.source_app_user_model_id

    if session:  # there needs to be a media session running
        if session.source_app_user_model_id == TARGET_ID:
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
            # converts winrt vector to list
            info_dict['genres'] = list(info_dict['genres'])
            return info_dict
    raise Exception('TARGET_PROGRAM is not the current media session')


if __name__ == '__main__':
    print(json.dumps(get_media_info(), indent=4, sort_keys=True, default=str))
    
