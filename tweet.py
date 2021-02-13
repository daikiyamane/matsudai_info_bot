#coding; utf-8

import os
import tweepy

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


retweet_favorite()
