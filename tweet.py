#coding; utf-8

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

# 休校情報


def closed_school():
    url = "http://mobile.matsuyama-u.jp/mbl/hpg021101.htm?PSS=h132mjp8dm3iv02ob2c6ckbj5m&DATE="
    res = requests.get(url+f'{datetime.datetime.now().strftime("%Y%m%d")}')
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
        api.update_status(first)
        api.update_status(second)
    else:
        api.update_status(text)

# 補講情報


def supplementary_lecture():
    url = "http://mobile.matsuyama-u.jp/mbl/hpg021201.htm?PSS=h132mjp8dm3iv02ob2c6ckbj5m&DATE="
    res = requests.get(url+f'{datetime.datetime.now().strftime("%Y%m%d")}')
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
