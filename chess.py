import os
from dotenv import load_dotenv
from chessdotcom import get_player_profile, get_player_stats

class Chess:
    def __init__(self) -> None:
        self.username = os.getenv("username")

    load_dotenv()

    def get_profile(self):
        """
        :rtype dict
        """

        response_profile = get_player_profile(self.username)

        profile = {
            "avatar": response_profile.json['player']['avatar'],
            "player_id": response_profile.json['player']['player_id'],
            "username": response_profile.json['player']['username'],
            "title": "N/A",
            "followers": response_profile.json['player']['followers'],
            "last_online": response_profile.json['player']['last_online'],
            "is_streamer": response_profile.json['player']['is_streamer'],
            "twitch_url": "N/A"
        }

        if "title" in response_profile.json['player']:
            # Not everyone will have a title
            profile['title'] = response_profile.json['player']['title']

        if profile['is_streamer']:
            # Not everyone will have a twitch
            profile['twitch_url'] = response_profile.json['player']['twitch_url']

        return profile

    def get_stats(self):
        """
        :rtype dict
        """

        response_stats = get_player_stats(self.username)

        stats = {
            "highest_elo": response_stats.json['stats']['tactics']['highest']['rating'],
            "lowest_elo": response_stats.json['stats']['tactics']['lowest']['rating']
        }

        return stats
