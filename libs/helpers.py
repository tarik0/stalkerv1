# coding=utf-8
#!/usr/bin/env python3

from time import strftime
from colorama import init, Fore, Back, Style
from os import system, name

def clear_screen():
    system('cls' if name=='nt' else 'clear')

def get_max_line_length():
    return 30

def truncate(string, width):
    if len(string) > width:
        string = string[:width-3] + '...'
    return string

def ask(message):
    print("{0}[{1}]{2} [ ?? ] {3}{4}{5}: ".format(
        Style.BRIGHT + Fore.YELLOW,
        strftime("%d.%m.%y %X"),
        Fore.MAGENTA,
        Fore.WHITE,
        message,
        Style.RESET_ALL
    ), end="")
    tmp = input()
    return tmp

def success(message):
    print("{0}[{1}]{2} [ OK ] {3}{4}{5}".format(
        Style.BRIGHT + Fore.YELLOW,
        strftime("%d.%m.%y %X"),
        Fore.GREEN,
        Fore.WHITE + Style.BRIGHT,
        message,
        Style.RESET_ALL
    ))

def error(message):
    print("{0}[{1}]{2} [ ER ] {3}{4}{5}".format(
        Style.BRIGHT + Fore.YELLOW,
        strftime("%d.%m.%y %X"),
        Fore.RED,
        Fore.WHITE,
        message,
        Style.RESET_ALL
    ))

def info(message):
    print("{0}[{1}]{2} [INFO] {3}{4}{5}".format(
        Style.BRIGHT + Fore.YELLOW,
        strftime("%d.%m.%y %X"),
        Fore.CYAN,
        Fore.WHITE,
        message,
        Style.RESET_ALL
    ))

def print_logo():
    logo = """ 
           {cyan}/\/\{reset}
          {cyan}/    \{reset}        +-------------------------------------+
      {cyan}--+-------+--{reset}     |              {red}Stalker v1{reset}             |
        {cyan}|\ O O /|{reset}       +-------------------------------------+
      {cyan}__| \   / |__{reset}     |{yellow}Gelişmiş sosyal medya araştırma aracı{reset}|
     {cyan}/             \{reset}    +---+ {yellow}Geliştirici: Hichigo THT{reset} +------+
    {cyan}|               |{reset}       +--------------------------+
    {cyan}|               |{reset} {cyan}Telegram: @HichigoTHT{reset} {magenta}Instagram: @hichigo.exe{reset}

    """.format(cyan=Style.BRIGHT + Fore.CYAN, reset=Style.RESET_ALL, magenta=Style.BRIGHT + Fore.MAGENTA, yellow=Style.BRIGHT + Fore.YELLOW, red=Style.BRIGHT + Fore.RED)

    print(logo)