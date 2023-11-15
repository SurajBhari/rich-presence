from discordrp import Presence, PresenceError
import time
from get_info import get_media_info
import os 
import json
import yt_dlp

client_id = "1163238681088364584"  # Replace this with your own client id
last_track = None
download_songs = True # automatically download songs from youtube music
music_folder = os.environ.get("userprofile") + "/Music"

def is_playing(media_info):
    if not media_info:
        return False
    return int(media_info['playback_status']) == 4

def get_presence():
    while True:
        try:
            presence = Presence(client_id)
        except (FileNotFoundError, PresenceError):
            time.sleep(5)
            continue
        else:
            print(f"Connected to Discord")
            return presence


def download_song(url, output_folder="."):
    # Set options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(artist)s %(title)s.%(ext)s'),
        'quiet': 'true',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    presence = get_presence()
    while True:
        time.sleep(2)
        current_media_info=get_media_info()
        if not current_media_info or not is_playing(current_media_info) or not current_media_info['artist']:
            if last_track: # we should not spam the clear function if there was no song previously played
                print("No media playing, Cleaning up Presence.")
                try:
                    presence.clear()
                except OSError:
                    print("Discord have stopped responding")
                    presence = get_presence()
                    continue
                last_track = None
            continue
        if last_track == current_media_info['title']:
            continue
        end_time = current_media_info["end_time"] - current_media_info['position']
        start = int(time.time())
        end = int(time.time()) + end_time.seconds
        presence_data = {
            "state": current_media_info['artist'], # Note: This is the artist that is taken from windows. `artists` have more than one artist taken from yt
            "details": current_media_info['title'],
            "timestamps": {
                "start": start,
                "end": end, 
            },
            "assets": {
                "large_image": current_media_info['thumbnail'] or "https://media.tenor.com/15YUsMWt4FEAAAAi/music.gif",
            }
        }
        if end-start > 3590:
            del presence_data["timestamps"]
        if current_media_info["link"]: 
            presence_data["buttons"] = [
                {
                    "label": "Listen on YouTube",
                    "url": current_media_info["link"]
                }
            ]
        try:
            presence.set(presence_data)
        except OSError:
            print("Discord have stopped responding")
            presence = get_presence()
        print(f"Changed presence info to {current_media_info['artist']} - {current_media_info['title']}")
        last_track = current_media_info['title']
        # download the song 
        drp = f"{music_folder}/drp"
        if "drp" not in os.listdir(music_folder):
            os.makedirs(music_folder+"/drp")
        if "drp.json" not in os.listdir(music_folder+"/drp"):
            with open(music_folder+"/drp/drp.json", "w+") as f:
                json.dump({}, f)
        with open(music_folder+"/drp/drp.json", "r") as f:
            data = json.load(f)
        
        if current_media_info['id'] in data.keys():
            data[current_media_info['id']]['count'] += 1 
            data[current_media_info['id']]['time'].append(time.time())
        else:
            data[current_media_info['id']] = {
                "count": 1,
                "title": current_media_info['title'],
                "artist": current_media_info['artist'],
                "link": current_media_info['link'],
                "thumbnail": current_media_info['thumbnail'],
                "time": [time.time()]
            }
        # I tried to get the genre info too. but its not directly given
        with open(music_folder+"/drp/drp.json", "w") as f:
            json.dump(data, f, indent=4)
        if f"{current_media_info['artist']} {current_media_info['title']}.mp3" in os.listdir(drp):
            continue
        if not download_songs:
            continue
        if not current_media_info['link']:
            continue
        try:
            download_song(current_media_info['link'], drp)
        except Exception as e:
            print(e)
            continue
        