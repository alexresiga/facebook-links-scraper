import json
import re
import urllib.parse
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from domain.post import Post
from domain.track import Track
from domain.user import User

URL = 'https://l.facebook.com/l.php?u'


class Crawler:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-notifications")
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.actions = ActionChains(self.browser)
        self.browser.get('https://www.facebook.com/groups/1622209491386403/')
        self.filename = 'repo'

    def login(self):
        """
        Since the group is private and only members can see the posts i need to login first
        """
        my_email = os.getenv("EMAIL")  # use your own credentials
        my_pass = os.getenv("PASS")
        email = WebDriverWait(self.browser, 4).until(ec.visibility_of_element_located((By.ID, 'email')))
        email.send_keys(my_email)
        password = WebDriverWait(self.browser, 4).until(ec.visibility_of_element_located((By.ID, 'pass')))
        password.send_keys(my_pass + Keys.RETURN)

    @staticmethod
    def parse_url(url):
        """
        get user url without any bloat
        :param url: string
        :return: the url until the first '?'
        """
        try:
            pattern = re.compile("([^?]*)")
            result = pattern.search(url)
            return result.group(1)
        except TypeError:
            return None

    @staticmethod
    def parse_link(url):
        """
        get url of track without fbclid or any another tags
        :param url:
        :return:
        """
        try:
            pattern = re.compile("(.+?(?=fbclid))")
            result = pattern.search(url)
            return result.group(1).rstrip('?&')
        except TypeError:
            return None

    @staticmethod
    def parse_track_id(url):
        try:
            pattern = re.compile("(.+?(?=<span>))")
            result = pattern.search(url)
            return result.group(1)
        except TypeError:
            return None

    @staticmethod
    def get_emoji(element: WebElement):
        try:
            return element.find_element_by_tag_name('span').find_element_by_tag_name('span').get_attribute('innerHTML')
        except NoSuchElementException:
            return None

    def get_user(self, article: WebElement):
        name, user_link = [None] * 2
        try:
            name = article.find_element_by_css_selector('._5pb8.m_1djjlbjav._8o._8s.lfloat._ohe').get_attribute('title')
            user_link = self.parse_url(
                article.find_element_by_css_selector('._5pb8.m_1djjlbjav._8o._8s.lfloat._ohe').get_attribute('href'))
            b = article.find_element_by_css_selector('.igjjae4c.glosn74e.f2jdl7fy.cxfqmxzd').get_attribute("innerHTML")

            return User(user_link, name, b)
        except NoSuchElementException:
            return User(user_link, name)

    def get_track(self, article: WebElement):
        track_id, artwork, url = [None] * 3
        try:
            track_id_container = article.find_element_by_css_selector('.mbs._6m6._2cnj._5s6c')
            emoji = self.get_emoji(track_id_container.find_element_by_tag_name('a'))
            track_id = track_id_container.find_element_by_tag_name('a').get_attribute('innerHTML')
            track_id = re.sub('<span .+</span>', emoji, track_id) if emoji is not None else track_id
            artwork = article.find_element_by_css_selector('img.scaledImageFitWidth').get_attribute('src')
            url_map = urllib.parse.parse_qs(article.find_element_by_css_selector('a._52c6').get_attribute('href'))
            if URL not in url_map.keys():
                url = urllib.parse.unquote(article.find_element_by_css_selector('a._52c6').get_attribute('href'))
                url = self.parse_link(url)
            else:
                url = url_map[URL][0]
                url = self.parse_link(url)
            return Track(track_id, artwork, url)
        except NoSuchElementException:
            if track_id is None:
                url = article.find_element_by_css_selector('._5_jv._58jw').find_element_by_tag_name(
                    'a').get_attribute('innerHTML')
            return Track(track_id, artwork, url)

    @staticmethod
    def get_date(article: WebElement):
        return article.find_element_by_tag_name('abbr').get_attribute('title')

    @staticmethod
    def get_reactions(article: WebElement):
        try:
            r = article.find_element_by_css_selector('._81hb').get_attribute('innerHTML')
            return r
        except NoSuchElementException:
            return None

    def get_post(self, article):
        try:
            user = self.get_user(article)
            track = self.get_track(article)
            date = self.get_date(article)
            reactions = self.get_reactions(article)
            return Post(user, track, date, reactions)
        except NoSuchElementException:
            pass

    @staticmethod
    def save_posts(_json):
        _json['posts'] = _json['posts'][::-1]
        for post in _json['posts']:
            post['id'] = _json['posts'].index(post)
        with open('data.json', 'w') as g:
            json.dump(_json, g)

    def get_posts(self):
        """
        fetch all posts
        """
        self.login()
        post_n = 0
        data = {'posts': []}
        while True:
            try:
                element = self.browser.find_element_by_css_selector('._4-u2.mbm._4mrt._5jmm._5pat._5v3q._7cqq._4-u8')
                new_post = self.get_post(element)
                post_n += 1
                if new_post is not None:
                    new_post.id = post_n
                    data['posts'].append(vars(new_post))
                print("#{}".format(post_n))
                print(new_post)
                self.browser.execute_script('arguments[0].remove();', element)

                if post_n % 10 == 0:
                    self.actions.send_keys(Keys.ARROW_DOWN).perform()
            except NoSuchElementException:

                try:
                    WebDriverWait(self.browser, 30).until(ec.presence_of_element_located(
                        (By.CSS_SELECTOR, "._4-u2.mbm._4mrt._5jmm._5pat._5v3q._7cqq._4-u8")
                    ))
                except TimeoutException:
                    self.save_posts(data)
                    return
            except WebDriverException:
                self.save_posts(data)
                return

            except KeyboardInterrupt:
                self.save_posts(data)
                return


muzicantii = Crawler()
muzicantii.get_posts()
