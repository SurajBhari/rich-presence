import asyncio
from discordrp import Presence
import time


from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackInfo  as PlaybackInfo



async def get_media_info():
    sessions = await MediaManager.request_async()
    session = sessions.get_current_session()
    if not session:
        return None
    TARGET_ID = session.source_app_user_model_id

    if session:  # there needs to be a media session running
        if session.source_app_user_model_id == TARGET_ID:
            pinfo = session.get_playback_info()
            info = await session.try_get_media_properties_async()
            # song_attr[0] != '_' ignores system attributes
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
            info_dict['playback_status'] = pinfo.playback_status
            # converts winrt vector to list
            info_dict['genres'] = list(info_dict['genres'])
            return info_dict
    raise Exception('TARGET_PROGRAM is not the current media session')


if __name__ == '__main__':
    client_id = "1163238681088364584"  # Replace this with your own client id
    
