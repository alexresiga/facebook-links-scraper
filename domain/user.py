class User:
    def __init__(self, user_link, username, badge=None):
        self.__username = username
        self.__user_link = user_link
        self.__badge = badge

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def user_link(self):
        return self.__user_link

    @user_link.setter
    def user_link(self, value):
        self.__user_link = value

    @property
    def badge(self):
        return self.__badge

    @badge.setter
    def badge(self, value):
        self.__badge = value

    def __str__(self):
        return f'{self.username} -- {self.user_link}\nbadge: {self.badge}\nposted:\n'
