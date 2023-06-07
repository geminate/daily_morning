from datetime import date, datetime, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from zhdate import ZhDate
from dateutil.relativedelta import relativedelta

today = datetime.now() + timedelta(days = 1)

start_date = os.environ['START_DATE']
start_marry_date = os.environ['MARRY_START_DATE']
city = os.environ['CITY']
weatherKey = os.environ['WEATHER_KEY']
birthday_m = os.environ['BIRTHDAY_M']
birthday_d = os.environ['BIRTHDAY_D']
birthday = os.environ['BIRTHDAY']
birthday_child = os.environ['BIRTHDAY_CHILD']
birthday_child_date = os.environ['BIRTHDAY_CHILD_DATE']

marry = os.environ['MARRY']
last_day = os.environ['LAST_DAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://api.yytianqi.com/forecast7d?city=" + city + "&key=" + weatherKey
  res = requests.get(url).json()
  weather = res['data']['list'][0]

  weather_words = '今天的天气与你一样美好o(*￣▽￣*)ブ'
  weather_words_color = '#FA9F4E'

  wes = " 天气："+weather['tq1'] + "-" + weather['tq2']

  if wes.find('雨') != -1:
    weather_words = '今天有雨，亲爱的记得带伞~'
    weather_words_color = '#54D8FF'

  low_color = '#000000'
  high_color = '#000000'

  if math.floor(int(weather['qw2'])) <= 0:
    low_color = '#54D8FF'

  if math.floor(int(weather['qw1'])) >= 30:
    high_color = '#EE212D'

  return weather_words, weather_words_color, wes, " 最低气温：" + str(math.floor(int(weather['qw2']))), low_color," 最高气温："+ str(math.floor(int(weather['qw1']))), high_color

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return " 今天是我们恋爱的 第"+str(delta.days)+"天 "

def get_count2():
  delta = today - datetime.strptime(start_marry_date, "%Y-%m-%d")
  return  " 今天是我们结婚的 第"+str(delta.days)+"天 "

def get_count3():
  delta = today - datetime.strptime(birthday_child, "%Y-%m-%d")
  return  " 今天是筱玥出生的 第"+str(delta.days)+"天 "

def get_birthday():
  birth = ZhDate(today.year, int(birthday_m), int(birthday_d)).to_datetime()
  if birth < datetime.strptime(today.strftime('%Y-%m-%d'),"%Y-%m-%d"):
    birth = ZhDate(today.year + 1, int(birthday_m), int(birthday_d)).to_datetime()
  diff = birth.toordinal() - today.toordinal()
  if diff == 0:
    return {"value":" 今天是你的生日~ 生日快乐 ","color":"#FA9F4E"}
  return {"value":" 距离你的生日还有 " + str(diff) + "天 "}

def get_birthday2():
  next = datetime.strptime(str(today.year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.strptime(today.strftime('%Y-%m-%d'),"%Y-%m-%d"):
    next = next.replace(year=next.year + 1)
  diff = next.toordinal() - today.toordinal()
  if diff == 0:
    return {"value":" 今天是小刘的生日~ 祝他生日快乐 ","color":"#FA9F4E"}
  return {"value":" 距离小刘的生日还有 " + str(diff) + "天 "}

def get_birthday3():
  next = datetime.strptime(str(today.year) + "-" + birthday_child_date, "%Y-%m-%d")
  if next < datetime.strptime(today.strftime('%Y-%m-%d'),"%Y-%m-%d"):
    next = next.replace(year=next.year + 1)
  diff = next.toordinal() - today.toordinal()
  if diff == 0:
    return {"value":" 今天是筱玥的生日~ 祝他生日快乐 ","color":"#FA9F4E"}
  return {"value":" 距离筱玥的生日还有 " + str(diff) + "天 "}


def get_marry_left():
  next = datetime.strptime(str(today.year) + "-" + marry, "%Y-%m-%d")
  if next < datetime.strptime(today.strftime('%Y-%m-%d'),"%Y-%m-%d"):
    next = next.replace(year=next.year + 1)
  diff = next.toordinal() - today.toordinal()
  if diff == 0:
    return {"value":" 今天是我们两个的结婚纪念日~ 庆祝一下吧 ","color":"#FA9F4E"}
  return {"value":" 距离我们的结婚纪念日还有 " + str(diff) + "天 "}

def get_child_weeks():
  today = date.today()
  birthdate_obj = datetime.strptime(str(birthday_child), '%Y-%m-%d').date()

  rd = relativedelta(today, birthdate_obj)

  years = rd.years
  months = rd.months
  days = rd.days
  return {"value":" 筱玥已 "+ str(years) +"岁"+ str(months) + "月" + str(days) + "天 " }

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather_words, weather_words_color, weather, temp_low, temp_low_color, temp_high, temp_high_color = get_weather()
data = {"today":{"value":" "+ str(today.strftime('%Y-%m-%d'))+ " ","color":"#87CEEB"},"weather_words":{"value":weather_words,"color":weather_words_color} ,"weather":{"value":weather},"temp_low":{"value":str(temp_low) + '℃',"color":temp_low_color},"temp_high":{"value":str(temp_high) + '℃',"color":temp_high_color},"next_words":{"value":"每一天都值得铭记↓","color":"#FFB6C1"},"next_words2":{"value":"余生有幸和你在一起","color":"#FFB6C1"},"love_days":{"value":get_count()},"marry_days":{"value":get_count2()},"born_days":{"value":get_count3()},"birthday_left":get_birthday(),"birthday_left2":get_birthday2(),"birthday_left3":get_birthday3(),"marry_left":get_marry_left(),"child_weeks":get_child_weeks(),"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res = wm.send_template(user_id2, template_id, data)
print(res)
