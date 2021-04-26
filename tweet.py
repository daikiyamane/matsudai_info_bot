# coding; utf-8

import os
import tweepy
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time

auth = tweepy.OAuthHandler(
    os.environ["CONSUMER_KEY"], os.environ["CONSUMER_SECRET"])
auth.set_access_token(
    os.environ["ACCESS_TOKEN_KEY"], os.environ["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth)


def make_accounts():
    accounts = ["Matsudai_koho", "MU_Career",
                "MU_COOP", "MU_Renkei", "MU_Internation"]
    return accounts


def make_tweets(accounts, count, page):
    return [api.user_timeline(accounts[i], count=count, page=page) for i in range(len(accounts))]


def retweet_favorite():
    accounts = make_accounts()
    tweets = make_tweets(accounts, 5, 1)
    for tweet in tweets:
        for t in tweet:
            try:
                api.retweet(t.id)
            except tweepy.TweepError:
                print("すでにリツイートしてます")
            try:
                api.create_favorite(t.id)
            except tweepy.TweepError:
                print("すでにいいねしてます")


def get_url(url, status):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    a_tag = soup.find('a')
    today_url = "https://mobile.matsuyama-u.jp/mbl/" + a_tag.get('href')
    if today_url.split('=')[-1] == datetime.date.today().strftime('%Y%m%d'):
        return today_url
    else:
        if status == "cs":
            return "https://mobile.matsuyama-u.jp/mbl/hpg021101.htm?PSS=i525o5g0i0dlpr3r21h1gh07mg&DATE={}".format(datetime.date.today().strftime('%Y%m%d'))
        else:
            return "https://mobile.matsuyama-u.jp/mbl/hpg021201.htm?PSS=m438tgrrg6jpv9hits12lvku90&DATE={}".format(datetime.date.today().strftime('%Y%m%d'))

# 休校情報


def closed_school():
    url = get_url(
        "http://mobile.matsuyama-u.jp/mbl/hpg020101.htm?SETI=1", "cs")
    res = requests.get(url)
    if res.status_code == 404:
        api.update_status("今日の休講情報はありません")
        quit()
    soup = BeautifulSoup(res.text, 'html.parser')

    print(soup.prettify())

    for script in soup(["script", "style", "title", "a"]):
        script.decompose()
    print(soup)

    text = soup.get_text()

    lines = [line.strip() for line in text.splitlines()]
    print(lines)

    text = "\n".join(line for line in lines if line)
    print(text)
    if len(text) >= 140:
        first = text[:140]
        second = text[140:]
        api.update_status(second)
        api.update_status(first)
    else:
        api.update_status(text)


# 補講情報


def supplementary_lecture():

    url = get_url(
        "http://mobile.matsuyama-u.jp/mbl/hpg020201.htm?SETI=1", "sl")
    res = requests.get(url)
    if res.status_code == 404:
        api.update_status("今日の補講情報はありません")
        quit()
    soup = BeautifulSoup(res.text, 'html.parser')

    print(soup.prettify())

    for script in soup(["script", "style", "title", "a"]):
        script.decompose()
    print(soup)

    text = soup.get_text()

    lines = [line.strip() for line in text.splitlines()]
    print(lines)

    text = "\n".join(line for line in lines if line)
    print(text)
    if len(text) >= 140:
        first = text[:140]
        second = text[140:]
        api.update_status(first)
        api.update_status(second)
    else:
        api.update_status(text)


retweet_favorite()
if datetime.time(6, 00) <= datetime.datetime.now().time() and datetime.datetime.now().time() <= datetime.time(7, 0):
    closed_school()
    supplementary_lecture()
closed_school()
supplementary_lecture()
