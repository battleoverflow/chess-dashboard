"""
    Author: azazelm3dj3d (https://github.com/azazelm3dj3d)
    Project: Chess Dashboard (https://github.com/azazelm3dj3d/chess-dashboard)
    License: BSD 2-Clause
"""

import datetime
from flask import Flask, render_template, request
from chessdotcom import get_player_profile, get_player_stats
from chessdotcom.types import ChessDotComError

app = Flask(__name__)

def get_profile(username):
    """
    rtype dict
    """

    response_profile = get_player_profile(username)

    # Not all players will have a profile image
    try:
        player_avatar = response_profile.json['player']['avatar']
    except KeyError:
        player_avatar = "/static/img/missing_user.png"

    profile = {
        "avatar": player_avatar,
        "player_id": response_profile.json['player']['player_id'],
        "username": response_profile.json['player']['username'],
        "title": "N/A",
        "followers": response_profile.json['player']['followers'],
        "last_online": response_profile.json['player']['last_online'],
        "is_streamer": response_profile.json['player']['is_streamer'],
        "twitch_url": "https://www.twitch.tv"
    }

    if "title" in response_profile.json['player']:
        # Not everyone will have a title
        profile['title'] = response_profile.json['player']['title']

    if profile['is_streamer']:
        # Not everyone will have a twitch
        profile['twitch_url'] = response_profile.json['player']['twitch_url']

    return profile

def get_stats(username):
    """
    rtype dict
    """

    response_stats = get_player_stats(username)

    stats = {
        "highest_elo": response_stats.json['stats']['tactics']['highest']['rating'],
        "lowest_elo": response_stats.json['stats']['tactics']['lowest']['rating']
    }

    return stats

def calculate_increase(elo_values):
    try:
        # (abs(current_elo - previous_elo) / previous_elo) * 100.0
        percentage = (abs(elo_values[0] - elo_values[1]) / elo_values[1]) * 100.0
    except ZeroDivisionError:
        return 0

    return round(percentage, 2)

@app.route("/", methods=["POST", "GET"])
def index():
    username = 0

    if request.method == "POST":
        form_data = request.form

        for _, value in form_data.items():
            username = value
            break
    else:
        form_data = "N/A"

    try:
        chess_template = render_template(
            "index.html",
            form_data=form_data,
            avatar=get_profile(username)['avatar'],
            player_id=get_profile(username)['player_id'],
            username=get_profile(username)['username'],
            title=get_profile(username)['title'],
            followers=get_profile(username)['followers'],
            last_online=datetime.datetime.fromtimestamp(get_profile(username)['last_online']).strftime("%m/%d/%Y @ %H:%M:%S"),
            is_streamer=get_profile(username)['is_streamer'],
            twitch_url=get_profile(username)['twitch_url'],
            twitch_url_stripped=str(get_profile(username)['twitch_url']).replace("https://twitch.tv/", ""),
            highest_elo=get_stats(username)['highest_elo'],
            lowest_elo=get_stats(username)['lowest_elo'],
            elo_increase=calculate_increase([get_stats(username)['highest_elo'], get_stats(username)['lowest_elo']])
        )
    except ChessDotComError:
        chess_template = render_template(
            "index.html",
            avatar="/static/img/missing_user.png",
            player_id="N/A",
            username="N/A",
            title="N/A",
            followers="N/A",
            last_online="N/A",
            is_streamer="N/A",
            twitch_url="https://www.twitch.tv",
            highest_elo="N/A",
            lowest_elo="N/A",
            elo_increase="N/A"
        )

    return chess_template

if __name__ == "__main__":
    app.run()
