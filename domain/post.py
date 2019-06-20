from domain.user import User
from domain.track import Track


class Post:
    def __init__(self, _user: "User", _track: "Track", _date, _reactions, _id=None):
        self.id = _id
        self.username = _user.get_username()
        self.user_link = _user.get_user_link()
        self.badge = _user.get_badge()
        self.track_id = _track.get_track_id()
        self.artwork = _track.get_artwork()
        self.url = _track.get_url()
        self.date = _date
        self.reactions = _reactions

    def __str__(self):
        return "{} - {} - {}".format(self.username, self.track_id, self.date)
