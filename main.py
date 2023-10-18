import asyncio
from discordrp import Presence
import time
from get_info import get_media_info


client_id = "1163238681088364584"  # Replace this with your own client id
icon_name = "musical-note"
last_track = None

def is_playing(media_info):
    if not media_info:
        return False
    return int(media_info['playback_status']) == 4

if __name__ == '__main__':
    while True:
        try:
            presence = Presence(client_id)
        except FileNotFoundError:
            time.sleep(5)
            continue
        else:
            print(f"Connected to Discord")
            break
        
    while True:
        time.sleep(2)
        current_media_info=get_media_info()
        if not current_media_info or not is_playing(current_media_info):
            if last_track: # we should not spam the clear function if there was no song previously played
                print("No media playing, Cleaning up Presence.")
                presence.clear()
                last_track = None
            continue
        if last_track == current_media_info['title']:
            continue
        end_time = current_media_info["end_time"] - current_media_info['position']
        presence.set(
            {
                "state": current_media_info['artist'],
                "details": current_media_info['title'],
                "timestamps": {
                    "start": int(time.time()),
                    "end": int(time.time()) + end_time.seconds, 
                },
                "assets": {
                    "large_image": icon_name
                }
            }
        )
        print(f"Changed presence info to {current_media_info['artist']} - {current_media_info['title']}")
        last_track = current_media_info['title']