#!usr/bin/python
# -*- coding:utf-8 -*-
import json
import sqlite3
import requests
from datetime import datetime

def get_nowtime(type):
    nowtime = datetime.now()
    if type == 0:
        return nowtime
    elif type == 1:
        return str(nowtime.strftime("%Y年%m月%d日 %H时%M分%S秒"))   #nowtime_str
    elif type == 2:
        return str(nowtime.strftime("%Y-%m-%d"))                   #nowdate_str
    elif type == 3:
        return str(nowtime.strftime("%H:%M:%S"))                   #nowtime_str

def get_source(aid):
    api_url = "http://api.bilibili.com/archive_stat/stat?callback=&aid={0}".format(aid)
    DATE = get_nowtime(2)
    TIME = get_nowtime(3)
    response = requests.get(api_url).content

    jsDict = json.loads(response)
    print response

    code = jsDict['code']
    view = jsDict['data']['view']
    danmaku = jsDict['data']['danmaku']
    reply = jsDict['data']['reply']
    favorite = jsDict['data']['favorite']
    coin = jsDict['data']['coin']
    share = jsDict['data']['share']
    now_rank = jsDict['data']['now_rank']
    his_rank = jsDict['data']['his_rank']
    message = jsDict['message']

    conn = sqlite3.connect("bilibili.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS{0} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATE TEXT,
        TIME TEXT,
        code INT,
        view INT,
        danmaku INT,
        reply INT,
        favorite INT,
        coin INT,
        share INT,
        now_rank INT,
        his_rank INT,
        message TEXT);
        '''.format("`AV" + aid + "`"))

    c.execute("INSERT INTO "+ "`AV" + aid + "`" + " (DATE, TIME, code, view, danmaku, reply, favorite, coin, share, now_rank, his_rank, message) \
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (DATE, TIME, code, view, danmaku, reply, favorite, coin, share, now_rank, his_rank, message));

    conn.commit()
    conn.close()

get_source("8614334")
