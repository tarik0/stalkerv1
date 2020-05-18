# coding=utf-8
#!/usr/bin/env python3

from requests import Session, exceptions
from colorama import Style, Back
from libs.helpers import ask, info, error, success, truncate, get_max_line_length

SPOTIFY_GENERATE_TOKEN_API = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"

DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"

class SpotifyException(Exception):
    pass

class Spotify:
    def __init__(self, userid, proxies=None):
        self.session = Session()
        self.session.proxies, self.userid = proxies, userid
        self.session.headers.update({"User-Agent": DEFAULT_USER_AGENT})

        self.access_token, self.clientid = None, None

    def generate_api_token(self):
        self.session.get("https://open.spotify.com/user/" + self.userid)
        self.session.headers.update({
            "Host": "open.spotify.com",
            "Accept": "application/json",
            "Accept-Language": "en",
            "app-platform": "WebPlayer",
            "Referer": "https://open.spotify.com/user/" + self.userid,
            "Connection": "keep-alive"
        })
        
        response = self.session.get(SPOTIFY_GENERATE_TOKEN_API)
        
        if (response.status_code != 200):
            self.session.close()
            raise SpotifyException("Spotify erişim anahtarı alınamadı! (Status Code: {})".format(response.status_code))
        
        json_response = response.json()
        if ("accessToken" not in json_response or "clientId" not in json_response):
            self.session.close()
            raise SpotifyException("Spotify erişim anahtarı alınamadı! (Response içinde veri yok!)")
        
        self.access_token, self.clientid = json_response["accessToken"], json_response["clientId"]
    def get_playlists(self):
        self.session.headers.update({
            "Host": "api.spotify.com",
            "Accept": "application/json",
            "Accept-Language": "en",
            "app-platform": "WebPlayer",
            "Origin": "https://open.spotify.com",
            "Referer": "https://open.spotify.com/",
            "Connection": "keep-alive",
            "Authorization": "Bearer {}".format(self.access_token)
        })
        response = self.session.get("https://api.spotify.com/v1/users/{}/playlists".format(self.userid))

        if (response.status_code != 200):
            self.session.close()
            raise SpotifyException("Kullanıcının playlistleri alınamadı! (Status Code: {})".format(response.status_code))
        
        json_response = response.json()
        if ("href" not in json_response or "items" not in json_response):
            self.session.close()
            raise SpotifyException("Kullanıcının playlistleri alınamadı! (Response içinde veri yok!)")

        return json_response
    def get_playlist_info(self, playlistid):
        self.session.headers.update({
            "Host": "api.spotify.com",
            "Accept": "application/json",
            "Accept-Language": "en",
            "app-platform": "WebPlayer",
            "Origin": "https://open.spotify.com",
            "Referer": "https://open.spotify.com/",
            "Connection": "keep-alive",
            "Authorization": "Bearer {}".format(self.access_token)
        })
        response = self.session.get("https://api.spotify.com/v1/playlists/" + playlistid)

        if (response.status_code != 200):
            self.session.close()
            raise SpotifyException("{0} Id'li playlistin bilgileri alınamadı! (Status Code: {1})".format(playlistid, response.status_code))
        
        json_response = response.json()
        if ("tracks" not in json_response or "name" not in json_response):
            self.session.close()
            raise SpotifyException("{} Id'li playlistin bilgileri alınamadı! (Response içinde veri yok!)".format(playlistid))

        return json_response
    def get_user_info(self):
        self.session.headers.update({
            "Host": "api.spotify.com",
            "Accept": "application/json",
            "Accept-Language": "en",
            "app-platform": "WebPlayer",
            "Origin": "https://open.spotify.com",
            "Referer": "https://open.spotify.com/",
            "Connection": "keep-alive",
            "Authorization": "Bearer {}".format(self.access_token)
        })
        response = self.session.get("https://api.spotify.com/v1/users/{}".format(self.userid))

        if (response.status_code != 200):
            self.session.close()
            raise SpotifyException("Kullanıcının bilgileri alınamadı! (Status Code: {})".format(response.status_code))
        
        json_response = response.json()
        if ("display_name" not in json_response or "id" not in json_response):
            self.session.close()
            raise SpotifyException("Kullanıcının bilgileri alınamadı! (Response içinde veri yok!)")
        
        return json_response

def print_spotify(userid):
    try:
        info("Spotify profili alınıyor: {}".format(userid))
        spotify = Spotify(userid)
        spotify.generate_api_token()
        user_info = spotify.get_user_info()
        playlists = spotify.get_playlists()
    except SpotifyException as e:
        error(e)
        return
    except exceptions.ConnectionError:
        error("Spotify bağlantısı sağlanamadı! (ConnectionError)")
        return
      
    success("Spotify bilgileri yüklendi!\n")
    success("+======================Spotify Profil Bilgileri======================+")
    info("İsmi: {}".format(Back.GREEN + str(user_info["display_name"])))
    info("Hesap Türü: {}".format(Style.RESET_ALL + str(user_info["type"])))
    info("Takipçi Sayısı: {}".format(Style.RESET_ALL + str(user_info["followers"]["total"])))
    info("Profil Linki: {}".format(Style.RESET_ALL + str(user_info["external_urls"]["spotify"])))
    success("+====================================================================+")

    listened_artists = {}
    for playlist in playlists["items"]:
        try:
            playlist_info = spotify.get_playlist_info(playlist["id"])
        except SpotifyException as e:
            error(e)
            continue
        except exceptions.ConnectionError:
            error("Spotify bağlantısı sağlanamadı! (ConnectionError)")
            continue
        
        playlist_artists = {}
        for track in playlist_info["tracks"]["items"]:
            if (not track): continue
            if (not track["track"]): continue
            if (not track["track"]["album"]): continue
            if (not track["track"]["album"]["artists"]): continue

            for artist in track["track"]["album"]["artists"]:
                if (artist["name"] not in listened_artists):
                    listened_artists[artist["name"]] = 0
                else:
                    listened_artists[artist["name"]] = listened_artists[artist["name"]] + 1

                if (artist["name"] not in playlist_artists):
                    playlist_artists[artist["name"]] = 0
                else:
                    playlist_artists[artist["name"]] = playlist_artists[artist["name"]] + 1
        
        print("")
        success("Yeni bir playlist bulundu!")
        info("Adı: {}".format(Back.CYAN + playlist_info["name"]))
        info("Açıklaması: {}".format(Style.RESET_ALL + truncate(playlist_info["description"], get_max_line_length())))
        info("Spotify URI'si: {}".format(Style.RESET_ALL + playlist_info["uri"]))
        info("Takipçi Sayısı: {}".format(Style.RESET_ALL + str(playlist_info["followers"]["total"])))
        info("Toplam Şarkı Adeti: {}".format(Style.RESET_ALL + str(playlist_info["tracks"]["total"])))
        if(playlist_info["tracks"]["total"] == 0):
            continue
        elif (playlist_info["tracks"]["total"] < 3):
            info("Sondan Eklenen Şarkı: {0}-{1} [{2}]".format(
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][0]["track"]["album"]["artists"][0]["name"], get_max_line_length()),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][0]["track"]["album"]["name"], get_max_line_length() + 10),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][0]["added_at"], get_max_line_length())
            ))
        else:
            info("Sondan İlk Eklenen Şarkı: {0}-{1} [{2}]".format(
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][0]["track"]["album"]["artists"][0]["name"], get_max_line_length()),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][0]["track"]["album"]["name"], get_max_line_length()),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][0]["added_at"], get_max_line_length())
            ))
            info("Sondan İkinci Eklenen Şarkı: {0}-{1} [{2}]".format(
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][1]["track"]["album"]["artists"][0]["name"], get_max_line_length()),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][1]["track"]["album"]["name"], get_max_line_length()),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][1]["added_at"], get_max_line_length())
            ))
            info("Sondan Üçüncü Eklenen Şarkı: {0}-{1} [{2}]".format(
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][2]["track"]["album"]["artists"][0]["name"], get_max_line_length()),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][2]["track"]["album"]["name"], get_max_line_length()),
                truncate(Style.RESET_ALL + playlist_info["tracks"]["items"][2]["added_at"], get_max_line_length())
            ))

        info("Sanatçı listesi: {}".format(
            Style.RESET_ALL + ", ".join(playlist_artists.keys())
        ))

    top_listened_artist, top_listened_artist_value = "", 0
    for artist in listened_artists.keys():
        if (listened_artists[artist] > top_listened_artist_value):
            top_listened_artist = artist
            top_listened_artist_value = listened_artists[artist]

    print("")
    success("+========================Spotify Profil Özeti========================+")
    info("En Çok Şarkısı Eklenen Sanatçı: {}".format(Back.MAGENTA + top_listened_artist))
    info("Sanatçıdan eklenen şarkı sayısı: {}".format(Back.MAGENTA + str(top_listened_artist_value)))
    success("+====================================================================+")
