# Rich Presence: Stream Your Media to Discord Effortlessly

Experience a simple yet robust method to seamlessly stream your current running media to Discord. This utility leverages [winsdk](https://pypi.org/project/winsdk/), utilizing the power of [winrt](https://pypi.org/project/winrt/) to retrieve information about the media currently in use.

## Download

Download the latest version from the workflow artifacts on GitHub:

[![Package Application with Pyinstaller](https://github.com/SurajBhari/rich-presence/actions/workflows/main.yml/badge.svg)](https://github.com/SurajBhari/rich-presence/actions/workflows/main.yml)

## Additional Features

1. **Backup with `ytdlp`:** Utilizes `ytdlp` to download the current song in case of an internet outage, ensuring you can still enjoy your favorite tunes.
2. **Song Data Storage:** Keeps a record of the songs you've listened to, providing detailed statistics.
3. **Offline Functionality:** Downloading and storing song data works seamlessly even without an active Discord connection.

## Optional Customization

Feel free to personalize your experience by changing the `client_id` in `main.py` to your own client ID, allowing you to display your application name and icon.

## Build Instructions

Use the following commands to build the application:

- **Build with Console:**
  ```
  pyinstaller main.py --onefile -n "Discord Rich Presence" -i favicon.ico --collect-data ytmusicapi --add-data "favicon.ico;." --add-data "templates;templates"
  ```

- **Build without Console:**
  ```
  pyinstaller main.py --onefile -n "Discord Rich Presence" -i favicon.ico --collect-data ytmusicapi --noconsole --add-data "favicon.ico;." --add-data "templates;templates"
  ```

## Songs not detecting

If you are already listening to a song and open discord mid way. it will not change your presence until next song (can be also pausing and resuming the same song)

Alternatively

There is a weird bug with YTMusic. Some songs just doesn't come when searched for like [Challa from Jab Tak hai Jaan](https://music.youtube.com/watch?v=hhssZ5bDa8E) will not come up when [searched for](https://music.youtube.com/search?q=challa+rabbi). so my program would not be able to determine the thumbnail or link to that song.

## Virus Prompt

If you encounter a "Threats Found" prompt while using the no-console version, it's due to changes in Windows policy. Unfortunately, obtaining the necessary certificate for background execution is cost-prohibitive. To resolve this:
- Trust the application and make an exclusion in your defender settings.
- Alternatively, opt for the windowed version of the application.

Enjoy uninterrupted media streaming with Rich Presence!

---
