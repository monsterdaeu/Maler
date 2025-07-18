import os, re, sys, json, time, uuid, base64, zlib, shutil, tempfile, random, subprocess, platform, string
import requests
from bs4 import BeautifulSoup as parser

# Basic Colors
white = '\033[1;37m'
red = '\033[1;31m'
green = '\x1b[38;5;46m'
yellow = '\033[1;33m'
blue = '\033[1;34m'
orange = '\033[1;35m'
extra = '\x1b[38;5;208m'
black = "\033[1;30m"

# Logo
def logo():
    os.system("clear")
    print(f"""
{red}██████╗ ██╗      █████╗  ██████╗██╗  ██╗███╗   ███╗ █████╗ ██╗██╗     ███████╗██████╗     ██████╗  ██████╗ ███╗   ███╗██╗
{yellow}██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝████╗ ████║██╔══██╗██║██║     ██╔════╝██╔══██╗    ██╔══██╗██╔═══██╗████╗ ████║██║
{green}██████╔╝██║     ███████║██║     █████╔╝ ██╔████╔██║███████║██║██║     █████╗  ██████╔╝    ██████╔╝██║   ██║██╔████╔██║██║
{blue}██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██║╚██╔╝██║██╔══██║██║██║     ██╔══╝  ██╔══██╗    ██╔══██╗██║   ██║██║╚██╔╝██║██║
{yellow}██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██║ ╚═╝ ██║██║  ██║██║███████╗███████╗██║  ██║    ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║
{red}╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝

-------------------------------------------------
Owner            :           ROM1 BADMASH 
Github           :           ROMI D9D        
Version          :           0.69.091
Status           :           KING
""")
    print(54 * '-')


# Menu
def devi():
    logo()
    print("[1] Gallery pic")
    print("[2] Contact list")
    print("[E] Exit tool")
    print(54 * "-")
    okh = input("[?] Choose option : ")
    if okh in ["01", "1"]:
        main()
    elif okh in ["02", "2"]:
        login()
    elif okh in ["E", "e"]:
        exit()
    else:
        exit("[×] Re-run Commands")


def main():
    logo()
    cookies = input(' [?] Input Facebook cookies : ')
    logo()
    limit = int(input('[?] Limit of comments : '))
    logo()
    print('[*] Use comma to separate comments (e.g. hi bro,good)')
    print(54 * "-")
    text_comment = input('[?] Text comment : ')
    print(54 * "-")
    userid = input('[?] Post ID (e.g. 2551707761661610): ')
    with requests.Session() as x:
        x.headers.update({
            "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36",
            "referer": "https://www.facebook.com/",
            "origin": "https://business.facebook.com",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "accept": "*/*"
        })
        try:
            link = x.get("https://business.facebook.com/business_locations", cookies={'cookie': cookies})
            search = re.search(r"(EAAG\w+)", link.text).group(1)
            if 'EAAG' in search:
                comment(cookies, search, limit, text_comment, userid)
        except AttributeError:
            exit('\n [×] Invalid cookie or token not found')


def comment(coki, token, limit, text_comment, userid):
    a = 0
    for _ in range(limit):
        for z in text_comment.split(','):
            a += 1
            b = requests.post(f'https://graph.facebook.com/{userid}/comments/?message={z.strip()}&access_token={token}', cookies={'cookie': coki})
            if 'You can try again later' in b.text:
                exit('\n [×] Account restricted due to spam')
            if 'id' in b.text:
                print(f'\r[*] Total Comments: {a}', end=' ')
            else:
                continue


# Unique ID generation
try:
    user_login = os.getlogin()
except:
    user_login = "termux"

uuidd = str(os.geteuid()) + user_login + str(os.getuid())
id = "".join(uuidd).replace("_", "").replace("360", "AHS").replace("u", "9").replace("a", "A")
plat = platform.version()[14:][:21][::-1].upper() + platform.release()[5:][::-1].upper() + platform.version()[:8]
xp = plat.translate(str.maketrans('', '', ' -#:=.+;*()?=')).replace("  ", "")
bumper = f'{id}{xp}'

# Login & Shareing
ses = requests.Session()

def login():
    logo()
    cookie = input("[?] Put cookie : ")
    try:
        data = ses.get("https://business.facebook.com/business_locations", headers={
            "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; MI 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.86 Mobile Safari/537.36"
        }, cookies={"cookie": cookie})
        find_token = re.search(r"(EAAG\w+)", data.text)
        open("token.txt", "w").write(find_token.group(1))
        open("cookie.txt", "w").write(cookie)
        menu()
    except:
        os.system("rm token.txt cookie.txt")
        exit("[×] Maybe cookies expired or invalid")


def menu():
    try:
        token = open("token.txt", "r").read()
        cok = open("cookie.txt", "r").read()
        cookie = {"cookie": cok}
        nama = ses.get(f"https://graph.facebook.com/me?fields=name&access_token={token}", cookies=cookie).json()["name"]
    except:
        login()
    logo()
    print(f"[❤] Welcome {nama} to Sharing Tool")
    print(54 * "-")
    idt = input("[>] Put Post Full Link (or ID): ")
    print(54 * "-")
    limit = int(input("[?] Sharing limit: "))
    logo()
    try:
        for n in range(1, limit + 1):
            post = ses.post(
                f"https://graph.facebook.com/v13.0/me/feed?link={idt}&published=0&access_token={token}",
                headers={"user-agent": "Mozilla/5.0"},
                cookies=cookie
            ).text
            data = json.loads(post)
            if "id" in data:
                print(f"[{n}] Successfully shared: {data['id']}")
            else:
                exit("[×] Cookie expired or incorrect post link")
    except:
        exit("[×] Cookie expired or network error")


if __name__ == '__main__':
    devi()
