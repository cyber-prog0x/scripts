#!/usr/bin/env python3

import requests
import socket
import socks
import time
import wget
import re

def download(url, file_name):
    wget.download(url, file_name)

def crawl_body(url):
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7891)
    socket.socket = socks.socksocket
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        body = r.text
        match = re.search(r'(https.*mp3)\"', body, re.M | re.I)
        if match:
            #  print(match.group(1))
            fileUrl = match.group(1)
            filename = "./data/{0}".format(fileUrl.split("/")[-1])
            download(fileUrl, filename)
        else:
            print("no match!")
    except:
        print("[ERR]: craw body exception!")


def find_link_in_everypage(pageUrl):
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7891)
    socket.socket = socks.socksocket
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        r = requests.get(pageUrl, headers=headers)
        body = r.text
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', body)
        article_url_list = []
        for url in urls:
            if "/VOA_Standard_English/" in url and len(url) > len("/VOA_Standard_English/"):
                print("Find article url: ", url)
                article_url_list.append(url)

        return article_url_list
    except:
        print("[ERR]: find link exception!")
        return []
            

def index():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7891)
    socket.socket = socks.socksocket
    url_list = []
    index_url = "https://www.51voa.com/VOA_Standard_1.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        r = requests.get(index_url, headers=headers)
        body = r.text
        #  print(body)
        urls = re.findall(r'href=[\'"]?([^\'" >]+)', body)
        for url in urls:
            if "VOA_Standard_" in url and "VOA_Standard_English" not in url:
                url_list.append(url)
        return url_list
    except:
        return []

if __name__ == "__main__":
    url = "https://www.51voa.com/VOA_Standard_English/icrc-laws-war-remain-relevant-today-despite-new-challenges-82663.html"
    #  crawl_body(url)
    #  for url in index():
        #  if "/" not in url:
            #  cawurl = "https://www.51voa.com/{0}".format(url)
            #  print("crawl page: ", cawurl)
            #  article_url_list = find_link_in_everypage(cawurl)
            #  for each_article in article_url_list:
                #  time.sleep(1)
                #  fullUrl = "https://www.51voa.com{0}".format(each_article)
                #  print("[INFO] working page: ", fullUrl)
                #  crawl_body(fullUrl)

    for i in range(10, 36):
        cawurl = "https://www.51voa.com/VOA_Standard_{0}.html".format(str(i))
        print("working: page ", cawurl)
        article_url_list = find_link_in_everypage(cawurl)
        for each_article in article_url_list:
            fullUrl = "https://www.51voa.com{0}".format(each_article)
            print("[INFO] working page: ", fullUrl)
            crawl_body(fullUrl)


