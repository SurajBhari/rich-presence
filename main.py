from discordrp import Presence, PresenceError
import time
from get_info import get_media_info
import os 
import json
import yt_dlp
import pystray
import PIL.Image

enabled = True # if false the program is disabled and will not do anything 
client_id = "1163238681088364584"  # Replace this with your own client id
last_track = None
download_songs = True # automatically download songs from youtube music
use_discord = True # use discord rich presence if not then just logs your songs and downlaods them
music_folder = os.environ.get("userprofile") + "/Music"
strict_mode = True # if true it will only show the media that are detected as songs. if false it will show all media that are playing

def is_playing(media_info):
    if not media_info:
        return False
    return int(media_info['playback_status']) == 4

def get_presence():
    if not use_discord:
        return None
    try:
        presence = Presence(client_id)
    except (FileNotFoundError, PresenceError):
        return None
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


if __name__ != '__main__':
    exit(-1) # this file should not be imported

image = PIL.Image.open("favicon.ico")


def after_click(icon, query):
    global strict_mode, use_discord, download_songs
    if query.text == "Strict Mode":
        strict_mode = not strict_mode
        query.checked = strict_mode
    elif query.text == "Enable Presence":
        use_discord = not use_discord
        query.checked = use_discord
    elif query.text == "Download Songs":
        download_songs = not download_songs
        query.checked = download_songs
    elif query.text == "Exit":
        icon.stop()
    elif query.text == "Enable":
        enabled = not enabled
        query.checked = enabled
    else:
        print(query.text)
        

menu = pystray.Menu(
    pystray.MenuItem("Enable", after_click, default=enabled),
    pystray.MenuItem("Strict Mode", after_click, default=strict_mode),
    pystray.MenuItem("Enable Presence", after_click, default=use_discord),
    pystray.MenuItem("Download Songs", after_click, default=download_songs),
    pystray.MenuItem("Exit", after_click)
    )

icon = pystray.Icon(
    "DRP", 
    image, 
    "Discord Rich Presence", 
    menu=menu)

print(dir(icon))
#icon.run()


presence = get_presence()

while True:
    if not enabled:
        continue
    time.sleep(2)
    if not presence:
        presence = get_presence()
    current_media_info=get_media_info()
    if not current_media_info['id'] and strict_mode:
        print("Strict mode is enabled. Skipping non song media")
        current_media_info = None
    if not current_media_info or not is_playing(current_media_info) or not current_media_info['artist']:
        if last_track: # we should not spam the clear function if there was no song previously played
            print("No media playing, Cleaning up Presence.")
            if presence:
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
    if not current_media_info['id']:
        del presence_data["timestamps"] # if there is no id. then its not a song. then we should not show the timestamps
    if current_media_info["link"]: 
        presence_data["buttons"] = [
            {
                "label": "Listen on YouTube",
                "url": current_media_info["link"]
            }
        ]
    if presence:
        if strict_mode and not current_media_info['id']:
            print(f"Strict mode is enabled. Skipping {current_media_info['artist']} - {current_media_info['title']}")
            continue
        try:
            presence.set(presence_data)
        except OSError:
            print("Discord have stopped responding")
        print(f"Changed presence info to {current_media_info['artist']} - {current_media_info['title']}")
    else:
        print(f"Discord not connected. Doing other stuff regardless. {current_media_info['artist']} - {current_media_info['title']}")
    last_track = current_media_info['title']
    drp = f"{music_folder}/drp"
    if "drp" not in os.listdir(music_folder):
        os.makedirs(music_folder+"/drp")

    if not current_media_info['id']:
        continue

    if "drp.json" not in os.listdir(music_folder+"/drp"):
        with open(music_folder+"/drp/drp.json", "w+") as f:
            json.dump({}, f)
    with open(music_folder+"/drp/drp.json", "r") as f:
        data = json.load(f)
        
    if current_media_info['id'] in data.keys():
        if current_media_info['position'].seconds < 5:
            # it means that the current song is just started and not resumed.
            data[current_media_info['id']]['count'] += 1 
            data[current_media_info['id']]['time'].append(time.time())
    else:
        data[current_media_info['id']] = {
            "count": 1,
            "title": current_media_info['title'],
            "artists": current_media_info['artists'],
            "artist": current_media_info['artist'],
            "link": current_media_info['link'],
            "thumbnail": current_media_info['thumbnail'],
            "time": [time.time()]
        }
    # I tried to get the genre info too. but its not directly given
    with open(music_folder+"/drp/drp.json", "w") as f:
        json.dump(data, f, indent=4)
    # download the song 
    if f"{current_media_info['artist']} {current_media_info['title']}.mp3" in os.listdir(drp):
        continue
    if not download_songs:
        continue
    try:
        download_song(current_media_info['link'], drp)
    except Exception as e:
        print(e)
        continue
        