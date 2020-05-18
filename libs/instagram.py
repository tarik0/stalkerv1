# coding=utf-8
#!/usr/bin/env python3

from requests import Session, exceptions
from colorama import Style, Back
from libs.helpers import ask, info, error, success, truncate, get_max_line_length

INSTAGRAM_USER_INFO_URL = "https://www.instagram.com/{}/?__a=1"

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"

class InstagramException(Exception):
    pass

class Instagram:
    def __init__(self, username):
        self.username = username
        self.session = Session()
        self.session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

    def get_user_info(self):
        response = self.session.get(INSTAGRAM_USER_INFO_URL.format(self.username))

        if (response.status_code != 200):
            raise InstagramException("Instagram'a bağlanılamıyor! (Status Code: {})".format(response.status_code))

        json_response = response.json()
        if ("graphql" not in json_response):
            raise InstagramException("Instagram'dan veri alınamıyor! (Response içinde veri yok!)")
            
        return json_response


def print_instagram(username):
    try:
        info("Instagram kullanıcısının bilgileri alınıyor: {}".format(username))
        instagram = Instagram(username)
        user_info = instagram.get_user_info()
    except InstagramException as e:
        error(e)
        return
    except exceptions.ConnectionError:
        error("Spotify bağlantısı sağlanamadı! (ConnectionError)")
        return

    is_private = "Herkese Açık"
    if (user_info["graphql"]["user"]["is_private"]):
        is_private = "Gizli Hesap"

    is_verified = "Hayır"
    if (user_info["graphql"]["user"]["is_verified"]):
        is_verified = "Evet"

    facebook_address = "Yok"
    if (user_info["graphql"]["user"]["connected_fb_page"]):
        facebook_address = str(user_info["graphql"]["user"]["connected_fb_page"])

    success("Instagram bilgileri yüklendi!\n")
    success("+=====================Instagram Profil Bilgileri=====================+")
    info("Tam İsmi: {}".format(Back.MAGENTA + str(user_info["graphql"]["user"]["full_name"])))
    info("Kullanıcı Adı: {}".format(Style.RESET_ALL + username))
    info("Hesabın Instagram ID'si: {}".format(Style.RESET_ALL + user_info["graphql"]["user"]["id"]))
    info("Biyografisi: {}".format(Style.RESET_ALL + user_info["graphql"]["user"]["biography"]))
    info("Takip Edilen Hesap Sayısı: {}".format(Style.RESET_ALL + str(user_info["graphql"]["user"]["edge_followed_by"]["count"])))
    info("Takip Eden Hesap Sayısı: {}".format(Style.RESET_ALL + str(user_info["graphql"]["user"]["edge_follow"]["count"])))
    info("Hesap durumu: {}".format(Style.RESET_ALL + is_private))
    info("Hesap onaylanma durumu: {}".format(Style.RESET_ALL + is_verified))
    info("Bağlı Facebook Hesabı: {}".format(Style.RESET_ALL + facebook_address))
    success("+====================================================================+")
