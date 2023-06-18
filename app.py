import datetime
from flask import Flask, render_template
from chess import Chess

app   = Flask(__name__)
chess = Chess()

@app.route("/")
def index():
    chess_template = render_template(
        "index.html", # Template
        avatar=chess.get_profile()['avatar'],
        player_id=chess.get_profile()['player_id'],
        username=chess.get_profile()['username'],
        title=chess.get_profile()['title'],
        followers=chess.get_profile()['followers'],
        last_online=datetime.datetime.fromtimestamp(chess.get_profile()['last_online']).strftime("%m/%d/%Y @ %H:%M:%S"),
        is_streamer=chess.get_profile()['is_streamer'],
        twitch_url=chess.get_profile()['twitch_url'],
        highest_elo=chess.get_stats()['highest_elo'],
        lowest_elo=chess.get_stats()['lowest_elo']
    )

    return chess_template

if __name__ == "__main__":
    app.run(debug=True)
