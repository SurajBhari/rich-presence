# Rich Presence

A simple robust way of streaming your current running media to Discord.

Utilizes [winsdk](https://pypi.org/project/winsdk/) which uses [winrt](https://pypi.org/project/winrt/) under the hood to get info of current running media.

# Download
Download from the latest workfrom from ->
[![Package Application with Pyinstaller](https://github.com/SurajBhari/rich-presence/actions/workflows/main.yml/badge.svg)](https://github.com/SurajBhari/rich-presence/actions/workflows/main.yml)


# Optional
Change the `client_id` in `main.py` to your own client id to get your own application name and icon.

# Build Instructions
`pyinstaller ./src/main.py --onefile -n "Discord Rich Presence" -i favicon.ico --collect-data ytmusicapi` - Builds with console 
`pyinstaller ./src/main.py --onefile -n "Discord Rich Presence" -i favicon.ico --collect-data ytmusicapi --noconsole` - Builds with no console 

# Virus prompt
If you are trying to use the no console version then you must have gotten a prompt saying `Threats Found` </br>
Since windows have changed their policy and requires me to have a certificate which cost 100's of dollars per year to sign this app so that it can run in background. I am not able to do it.</br>
If you trust me then you can make an exclusion in your defender to run this or just simply use windowed version </br>

