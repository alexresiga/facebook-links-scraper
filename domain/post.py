from domain.track import Track
from domain.user import User


class Post:
    def __init__(self, user: "User", track: "Track", date, reactions, post_id=None):
        self.id = post_id
        self.username = user.username
        self.user_link = user.user_link
        self.badge = user.badge
        self.track_id = track.track_id
        self.artwork = track.artwork
        self.url = track.url
        self.date = date
        self.reactions = reactions

    def __str__(self):
        return f'{self.username} - {self.track_id} - {self.date}'
