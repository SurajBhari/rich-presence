import asyncio
from discordrp import Presence
import time
from get_info import get_media_info


client_id = "1163238681088364584"  # Replace this with your own client id
last_track = None

def is_playing(media_info):
    return int(media_info['playback_status']) == 4

if __name__ == '__main__':
    with Presence(client_id) as presence:
        while True:
            time.sleep(2)
            current_media_info = asyncio.run(get_media_info())
            if not any([current_media_info, is_playing(current_media_info)]):
                print("No media playing")
                presence.clear()
                last_track = None
                continue
            if last_track == current_media_info['title']:
                continue
            presence.set(
                {
                    "state": current_media_info['artist'],
                    "details": current_media_info['title'],
                    "timestamps": {
                        "start": int(time.time())
                    },
                    "assets": {
                        "large_image": "musical-note"
                    }
                }
            )
            last_track = current_media_info['title']