from matplotlib.pyplot import *
import numpy
import json
import os 
from datetime import datetime
from flask import render_template, render_template_string, app, Flask

drp = os.environ.get("userprofile") + "/Music/drp/drp.json"

with open(drp, "r") as f:
    data = json.load(f)

"""
{
    "6cucosmPj-A": {
        "count": 2,
        "title": "Every Breath You Take",
        "artists": [
            {
                "name": "The Police",
                "id": "UCbsRGw640UF_F7AIwHW-zmg"
            }
        ],
        "artist": "The Police",
        "link": "https://music.youtube.com/watch?v=6cucosmPj-A",
        "thumbnail": "https://lh3.googleusercontent.com/OypoT7E9cuMpyxKX4Xd03-OWwwVoo5qHUwCnnRCZO2NCym6vA65l2hQ9fYD0fpJcb9wmGHNV9kd38E8=w120-h120-s-l90-rj",
        "time": [
            1700082682.8302255,
            1700082730.4788535
        ]
    }
}
"""
artists_dict = {}
times = []
for song in data.values():
    for time in song["time"]:
        times.append(time)
    artists = song.get("artists")
    if not artists:
        continue
    for artist in artists:
        if artist["name"] in artists_dict:
            artists_dict[artist["name"]] += 1
        else:
            artists_dict[artist["name"]] = 1


def show_stats():
    global data, artists_dict, times
    top_10_songs = sorted(data.values(), key=lambda x: x["count"], reverse=True)[:10]
    top_10_artists = sorted(artists_dict.items(), key=lambda x: x[1], reverse=True)[:10]
    # plot the time graph
    # day by day
    times = sorted(times)
    times = [datetime.fromtimestamp(time) for time in times]
    times = [time.strftime("%Y-%m-%d") for time in times]
    times = [datetime.strptime(time, "%Y-%m-%d") for time in times]
    dic = {}
    for time in times:
        if time in dic:
            dic[time] += 1
        else:
            dic[time] = 1
    x = list(dic.keys())
    y = list(dic.values())
    plot(x, y)
    savefig("time.png")
    app = Flask(__name__)
    with app.app_context():
        html =  render_template("one.html", 
                                top_songs=top_10_songs, 
                                top_artists=top_10_artists, 
                                trend_graph="time.png"
                                ) 
    with open("temp.html", "w") as f:
        f.write(html)
    os.system("start temp.html")

    
if __name__ == "__main__":
    show_stats()