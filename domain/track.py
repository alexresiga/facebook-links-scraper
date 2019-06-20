import html


class Track:
    def __init__(self, _track_id, _artwork, _url=None):
        self.__track_id = _track_id
        self.__artwork = _artwork
        self.__url = _url

    def get_track_id(self):
        return html.unescape(self.__track_id) if self.__track_id is not None else None

    def set__track_id(self, t):
        self.__track_id = t

    def get_artwork(self):
        return self.__artwork

    def set_artwork(self, art):
        self.__artwork = art

    def get_url(self):
        return self.__url

    def set_url(self, u):
        self.__url = u

    def __str__(self):
        return "track id: {}\nurl: {}\nartwork: {}".format(self.get_track_id(), self.get_url(), self.get_artwork())
