from discordrp import Presence, PresenceError
import time
from get_info import get_media_info, populate_yt
import os
import json
import yt_dlp
import pystray
import PIL.Image
from typing import Optional, Union
from stats import show_stats
from win11toast import toast, notify
import sys

client_id = "1163238681088364584"  # Replace this with your own client id
last_track = None
last_state = None
music_folder = os.environ.get("userprofile") + "/Music"
default_icon = "https://media.tenor.com/15YUsMWt4FEAAAAi/music.gif"
play_image = ""  # we don't need to prevent obstruction to thumbnail. but you can add one if you wish to.
pause_image = "https://cdn.iconscout.com/icon/free/png-512/free-pause-circle-round-resume-play-player-30539.png?f=webp&w=256"


# settings | These are default settings. changing these will not change anything. the program remembers the settings in a json file
enabled = True  # if false the program is disabled and will not do anything
download_songs = True  # automatically download songs from youtube music
use_discord = True  # use discord rich presence if not then just logs your songs and downlaods them
strict_mode = False  # if true it will only show the media that are detected as songs. if false it will show all media that are playing
show_notification = True  # if true it will show a notification when song changes

template_settings = {
    "enabled": enabled,
    "download_songs": download_songs,
    "use_discord": use_discord,
    "strict_mode": strict_mode,
    "show_notification": show_notification,
}

if "drp" not in os.listdir(music_folder):
    os.makedirs(music_folder + "/drp")

if "settings.json" not in os.listdir(music_folder + "/drp"):
    json.dump(
        template_settings, open(music_folder + "/drp/settings.json", "w+"), indent=4
    )
    print("Settings file not found. Creating one with default settings")

try:
    with open(music_folder + "/drp/settings.json", "r") as f:
        settings = json.load(f)
except:
    settings = template_settings

enabled = settings["enabled"]
download_songs = settings["download_songs"]
use_discord = settings["use_discord"]
strict_mode = settings["strict_mode"]
show_notification = settings["show_notification"]

if "drp.json" not in os.listdir(music_folder + "/drp"):
    with open(music_folder + "/drp/drp.json", "w+") as f:
        json.dump({}, f)
with open(music_folder + "/drp/drp.json", "r") as f:
    data = json.load(f)


def is_playing(media_info) -> bool:
    if not media_info:
        return False
    return int(media_info["playback_status"]) == 4


def get_presence() -> Optional[Presence]:
    if not use_discord:
        return None
    try:
        presence = Presence(client_id)
    except (FileNotFoundError, PresenceError):
        return None
    else:
        print(f"Connected to Discord")
        return presence


def download_song(url, output_folder=".") -> None:
    # Set options for yt-dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_folder, "%(artist)s %(title)s.%(ext)s"),
        "quiet": "true",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def send_notification(title, image_link, small_content=None):
    image_link = image_link.split("=w120")[0]
    if sys.getwindowsversion().build >= 22000:
        # windows 11
        icon = {"src": image_link, "placement": "hero"}
        notify(
            title,
            small_content,
            icon=icon,
            app_id="Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic",
            audio={"silent": "true"},
            duration="short",
        )
    else:
        icon.notify(small_content, title)


if __name__ != "__main__":
    exit(-1)  # this file should not be imported

try:
    image = PIL.Image.open("favicon.ico")
except FileNotFoundError:  # fix this later
    import requests

    try:
        image = PIL.Image.open(
            requests.get(
                "http://surajbhari.info:666/static/favicon.ico", stream=True
            ).raw
        )
    except Exception as e:
        image = PIL.Image.open(
            requests.get("https://www.youtube.com/favicon.ico", stream=True).raw
        )


def after_click(icon: pystray.Icon, query: pystray.MenuItem) -> None:
    global strict_mode, use_discord, download_songs, enabled, show_notification, settings, music_folder
    if query.text == "Strict Mode":
        strict_mode = not strict_mode
        print(f"Strict mode is now {strict_mode}")
        settings["strict_mode"] = strict_mode
        json.dump(settings, open(music_folder + "/drp/settings.json", "w+"), indent=4)

    elif query.text == "Enable Presence":
        use_discord = not use_discord
        print(f"Discord presence is now {use_discord}")
        settings["use_discord"] = use_discord
        json.dump(settings, open(music_folder + "/drp/settings.json", "w+"), indent=4)

    elif query.text == "Download Songs":
        download_songs = not download_songs
        print(f"Download songs is now {download_songs}")
        settings["download_songs"] = download_songs
        json.dump(settings, open(music_folder + "/drp/settings.json", "w+"), indent=4)

    elif query.text == "Exit":
        icon.stop()
        os._exit(0)
    elif query.text == "Enable":
        enabled = not enabled
        print(f"Enabled is now {enabled}")
        settings["enabled"] = enabled
        json.dump(settings, open(music_folder + "/drp/settings.json", "w+"), indent=4)
    elif query.text == "Show Notifications":
        show_notification = not show_notification
        print(f"Show Notifications is now {show_notification}")
        settings["show_notification"] = show_notification
        json.dump(settings, open(music_folder + "/drp/settings.json", "w+"), indent=4)
    elif query.text == "Show Stats":
        show_stats()
    elif query.text == "Show current notification":
        string = "No Media playing"
        thumbnail = ""
        if last_track:
            string = f"{current_media_info['artist']} - {current_media_info['title']}"
            thumbnail = current_media_info["thumbnail"]

        send_notification(string, thumbnail)
    else:
        print(query.text)


menu = pystray.Menu(
    pystray.MenuItem("Enable", after_click, checked=lambda item: enabled),
    pystray.MenuItem("Strict Mode", after_click, checked=lambda item: strict_mode),
    pystray.MenuItem("Enable Presence", after_click, checked=lambda item: use_discord),
    pystray.MenuItem(
        "Download Songs", after_click, checked=lambda item: download_songs
    ),
    pystray.MenuItem(
        "Show Notifications", after_click, checked=lambda item: show_notification
    ),
    pystray.MenuItem("Show Stats", after_click),
    pystray.MenuItem(
        "Show current notification", after_click, default=True, visible=False
    ),
    pystray.MenuItem("Exit", after_click),
)

icon = pystray.Icon("DRP", image, "Discord Rich Presence", menu=menu)


presence = get_presence()
icon.run_detached()


def update(media_info):
    end_time = media_info["end_time"] - media_info["position"]
    start = int(time.time())
    if not media_info["artist"]:
        media_info["artist"] = "Unknown Artist"
    if not media_info["title"]:
        media_info["title"] = "Unknown Title"
    presence_data = {
        "state": media_info[
            "artist"
        ],  # Note: This is the artist that is taken from windows. `artists` have more than one artist taken from yt
        "details": media_info["title"],
        "timestamps": {
            "start": start,  # I have tried to calculate the time but was unsuccesful as windows doesn't directly tell the current seek time.
        },
        "assets": {"large_image": media_info["thumbnail"] or default_icon},
    }
    if not is_playing(media_info):
        del presence_data["timestamps"]  # don't show how long we have been paused.
        presence_data["assets"]["small_image"] = pause_image
        presence_data["assets"]["small_text"] = "Paused"
    if media_info["link"]:
        presence_data["buttons"] = [
            {"label": "Listen on YouTube Music", "url": media_info["link"]}
        ]
    if presence and use_discord:
        if strict_mode and not media_info["id"]:
            print(
                f"Strict mode is enabled. Skipping {media_info['artist']} - {media_info['title']}"
            )
            return
        try:
            presence.set(presence_data)
        except Exception as e:
            print(f"Discord have stopped responding {e}")
        print(
            f"Changed presence info to {media_info['artist']} - {media_info['title']}"
        )
    else:
        print(
            f"Discord not connected. Doing other stuff regardless. {media_info['artist']} - {media_info['title']}"
        )


def record_playback(media_info):
    if media_info["id"] in data.keys():
        if media_info["position"].seconds < 5:
            # it means that the current song is just started and not resumed.
            data[media_info["id"]]["count"] += 1
            data[media_info["id"]]["time"].append(time.time())
    else:
        data[media_info["id"]] = {
            "count": 1,
            "title": media_info["title"],
            "artists": media_info["artists"],
            "artist": media_info["artist"],
            "link": media_info["link"],
            "thumbnail": media_info["thumbnail"],
            "time": [time.time()],
        }
    # I tried to get the genre info too. but its not directly given
    with open(music_folder + "/drp/drp.json", "w") as f:
        json.dump(data, f, indent=4)
    # download the song


def downlooad(media_info, drp):
    if f"{media_info['artist']} {media_info['title']}.webm" in os.listdir(drp):
        # Already downloaded
        print("Song Already downloaded")
        return
    if not download_songs:
        return
    try:
        download_song(media_info["link"], drp)
    except Exception as e:
        print(e)
        return


while True:
    if not enabled:
        continue
    time.sleep(2)
    print("HEARTBEAT")
    if not presence:
        presence = get_presence()
    current_media_info = get_media_info()
    if not current_media_info:
        continue  # how can i always forget this
    if (
        last_track == current_media_info["title"]
        and last_state == current_media_info["playback_status"]
    ):
        continue  # No change in media. paused is still paused. playing is still playing
    current_media_info = populate_yt(current_media_info)
    # Skip non-song media if strict mode is enabled and there is no 'id'
    if not current_media_info["id"] and strict_mode:
        print("Strict mode is enabled. Skipping non-song media.")
        current_media_info = None
        continue
    if show_notification:
        send_notification(
            f"{current_media_info['artist']} - {current_media_info['title']}",
            current_media_info["thumbnail"],
        )

    update(current_media_info)
    last_track = current_media_info["title"]
    last_state = current_media_info["playback_status"]
    drp = f"{music_folder}/drp"

    if not current_media_info["id"]:
        continue
    record_playback(current_media_info)
    downlooad(current_media_info, drp)
