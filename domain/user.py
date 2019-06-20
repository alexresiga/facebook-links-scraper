class User:
    def __init__(self, _user_link, _username, _badge=None):
        self.__username = _username
        self.__user_link = _user_link
        self.__badge = _badge

    def set_user_link(self, ul):
        self.__user_link = ul

    def get_user_link(self):
        return self.__user_link

    def get_username(self):
        return self.__username

    def set_username(self, u):
        self.__username = u

    def get_badge(self):
        return self.__badge

    def set_badge(self, b):
        self.__badge = b

    def __str__(self):
        return "{} -- {}\nbadge: {}\nposted:\n".format(self.get_username(), self.get_user_link(), self.get_badge())
