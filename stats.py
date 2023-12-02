import json
import os 
from datetime import datetime
from flask import render_template, render_template_string, app, Flask

drp = os.environ.get("userprofile") + "/Music/drp/drp.json"

def show_stats():
    with open(drp, "r") as f:
        data = json.load(f)
    for d in data:
        #"thumbnail": "https://lh3.googleusercontent.com/z8lL4eRXzWiYCve_kYLpAmFLNJjaEXziCaKmz3rhXijAJi38eybuDa-pVff6VWAXOC8rgUNgeIddHBE4=w120-h120-l90-rj",
        data[d]['thumbnail'] = data[d]['thumbnail'].split('=w120')[0]
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
    top_songs = sorted(data.values(), key=lambda x: x["count"], reverse=True)
    top_artists = sorted(artists_dict.items(), key=lambda x: x[1], reverse=True)
    # plot the time graph
    # day by day
    times = sorted(times)
    times = [datetime.fromtimestamp(time) for time in times]
    times = [time.strftime("%Y-%m-%d") for time in times]
    dic = {}
    for time in times:
        if time in dic:
            dic[time] += 1
        else:
            dic[time] = 1
    x = list(dic.keys())
    y = list(dic.values())
    app = Flask(__name__)
    # for piechart consider the first 8 artists. and others in others
    piechart_artists = top_artists[:40]
    piechart_artists.append(("others", sum([x[1] for x in top_artists[40:]])))

    with app.app_context():
        html =  render_template("one.html", 
                                top_songs=top_songs[:8], 
                                times = x,
                                counts = y,
                                piechart_artists=piechart_artists
                                ) 
    with open("temp.html", "w+") as f:
        f.write(html)
    os.system("start temp.html")

    
if __name__ == "__main__":
    show_stats()