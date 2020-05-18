# coding=utf-8
#!/usr/bin/env python3

from colorama import init, Style
from libs.spotify import print_spotify
from libs.instagram import print_instagram
from libs.helpers import ask, info, error, success, clear_screen, print_logo
from requests import exceptions
from os import _exit

import argparse

def parse_args():
    description = "Gelişmiş sosyal medya araştırma aracı.\n\nTurk Hack Team // Hichigo"
    parser = argparse.ArgumentParser(description=description, prog='stalker.py', add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    parser._optionals.title = "Opsiyonal araştırma methodları"
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Bu mesajı gösterir.')
    parser.add_argument("--spotify", help="Spotify hesabını araştırır.", default=None, metavar="[id]")
    parser.add_argument("--instagram", help="Instagram hesabını araştırır.", default=None, metavar="[user]")
    args = parser.parse_args()
    return args, parser

if __name__ == "__main__":
    init()
    clear_screen()
    print_logo()
    print(Style.BRIGHT)
    args, parser = parse_args()
    
    print(Style.RESET_ALL, end="")
    if (args.instagram == None and args.twitter == None and args.spotify == None and args.discord == None):
        parser.print_help()
        _exit(0)

    if (args.spotify):
        if (not args.spotify.startswith("spotify:user:")):
            print("Spotify profili bulunamadı!")

        print_spotify(args.spotify.replace("spotify:user:", ""))

    if (args.instagram):
        print_instagram(args.instagram)

    if (args.discord):
        if (not args.discord_auth_token):
            print("Discord ile araştırma yapmak için bir auth token ayarlamalısın!")
            parser.print_help()
            _exit(0)
        

        
