import html


class Track:
    def __init__(self, track_id, artwork, url=None):
        self.__track_id = track_id
        self.__artwork = artwork
        self.__url = url

    @property
    def track_id(self):
        return html.unescape(self.track_id) if self.track_id else None

    @track_id.setter
    def track_id(self, value):
        self.__track_id = value

    @property
    def artwork(self):
        return self.__artwork

    @artwork.setter
    def artwork(self, value):
        self.__artwork = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    def __str__(self):
        return f'track id: {self.track_id}\nurl: {self.url}\nartwork: {self.artwork}'
