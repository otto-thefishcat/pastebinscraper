import concurrent.futures
from threading import Thread
import requests
import json
import time
from colorama import Fore, init
init(convert=True)


def geturl():
    try:
        file = open("keywordfile.txt", "r").readlines()
    except:
        print("search.txt not found, make sure you have it in the same folder as the exe")
        time.sleep(10)
    write = open("urls.txt", "a+")
    for line in file:
        found = 0
        search = line.rstrip("\n")
        print(Fore.BLUE + f"searching {search}" + Fore.WHITE)
        r = requests.get(f"https://psbdmp.ws/api/v3/search/{search}")
        try:
            rjson = json.loads(r.text)
            sublist = rjson['data']
            for link in sublist:
                write.write(f"https://pastebin.com/raw/{link['id']}\n")
                found += 1
            print(Fore.GREEN + f"{search} got {found} urls")
        except:
            print(Fore.RED + "json error / no urls found")



def getwebsite(url):
    try:
        pagesource = requests.get(url).text
        if not "Not Found (#404)" in pagesource:
            return pagesource
        time.sleep(0.1)
    except:
        pass
    return ''


def start():
    geturl()
    Thread(target=write).start()
    global scraped
    scraped = []
    urls = open('urls.txt', 'r').read().splitlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        for value in zip(executor.map(getwebsite, urls)):
            try:
                scraped.append(str(value))
            except:
                continue
    while True:
        print("scraping finished, you may now close the program")
        time.sleep(10)


def write():
    while True:
        time.sleep(1)
        tempfile = open("scraped.txt", "a+", errors="ignore")
        tempfile.truncate(0)
        print(Fore.BLUE + "writing, do not close the program")
        tempfile.writelines(str(scraped).replace("\\\\r\\\\", "\n"))
        time.sleep(0.1)
        tempfile.close()
        print(Fore.LIGHTGREEN_EX + "wrote")
        time.sleep(3)


if __name__ == '__main__':
    start()
