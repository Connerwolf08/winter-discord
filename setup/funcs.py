import json
import pymysql
import asyncpraw
import random
import requests
import wikipedia
import http
import urllib

with open("./setup/config.json") as file_path:
    config = json.load(file_path)

# Database Functions

def db_write(query):
    with pymysql.connect(host=config["db"]["host"], user=config["db"]["username"], passwd=config["db"]["password"]) as con:
        cur = con.cursor()
        cur.execute(f"USE {config['db']['db_name']}")
        cur.execute(query)
        con.commit()
        print("[db_write] Query Executed")

def db_fetch(query):
    with pymysql.connect(host=config["db"]["host"], user=config["db"]["username"], passwd=config["db"]["password"]) as con:
        cur = con.cursor()
        cur.execute(f"USE {config['db']['db_name']}")
        cur.execute(query)
        res = cur.fetchone()
        print("[db_fetch] Query Executed")
        return res

def db_fetch_all(query):
    with pymysql.connect(host=config["db"]["host"], user=config["db"]["username"], passwd=config["db"]["password"]) as con:
        cur = con.cursor()
        cur.execute(f"USE {config['db']['db_name']}")
        cur.execute(query)
        res = cur.fetchone()
        print("[db_fetch_all] Query Executed")
        return res

# AsyncPraw api

async def praw_get(search):
    reddit = asyncpraw.Reddit(
        client_id = config["api"]["client_id"],
        client_secret = config["api"]["client_secret"],
        user_agent = config["api"]["user_agent"]
    )

    subreddit = await reddit.subreddit(search)
    all_subs = []
    hot = subreddit.hot(limit=50)
    async for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)
    return random_sub

# Tenor api

def tenor(search_term):
    apikey = config["api"]["tenor_key"]
    lmt = 50
    urls = []
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

    gifs = json.loads(r.content)
    for r in gifs["results"]:
        for m in r["media"]:
            g = m["gif"]
            res = g["url"]
            urls.append(res)
            
    
    return random.choice(urls)

# Wikipedia api

def wiki(search_term:str = None, lenght: int = None):
    try:
        obj = wikipedia.summary(f"'{search_term}'", lenght)
        return obj
    except Exception:
        obj = wikipedia.search(search_term)
        return obj

# Facts api

def fact(random_fact: bool = True):
    if random_fact:
        data = requests.get(url="https://uselessfacts.jsph.pl/random.json?language=en")
        api_data = json.loads(data.content)
        text = api_data["text"]
        return text

    else:
        data = requests.get(url="https://uselessfacts.jsph.pl/today.json?language=en")
        api_data = json.loads(data.content)
        text = api_data["text"]
        return text

# 8Ball api 

def ask_ball(query):
    conn = http.client.HTTPSConnection("8ball.delegator.com")
    question = urllib.parse.quote(query)
    conn.request('GET', '/magic/JSON/' + question)
    response = conn.getresponse()
    data = json.loads(response.read())
    return data["magic"]["answer"]

