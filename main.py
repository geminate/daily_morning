from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from zhdate import ZhDate

today = datetime.now()
start_date = os.environ['START_DATE']
start_marry_date = os.environ['MARRY_START_DATE']
city = os.environ['CITY']
birthday_m = os.environ['BIRTHDAY_M']
birthday_d = os.environ['BIRTHDAY_D']
birthday = os.environ['BIRTHDAY']
marry = os.environ['MARRY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]

  weather_words = '今天的天气与你一样美好o(*￣▽￣*)ブ'
  weather_words_color = '#FA9F4E'

  if weather['weather'].find('雨') != -1:
    weather_words = '今天有雨，亲爱的记得带伞~'
    weather_words_color = '#54D8FF'

  low_color = '#000000'
  high_color = '#000000'

  if math.floor(weather['low']) <= 0:
    low_color = '#54D8FF'

  if math.floor(weather['high']) >= 30:
    high_color = '#EE212D'

  return weather_words, weather_words_color, weather['weather'], math.floor(weather['low']), low_color, math.floor(weather['high']), high_color

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_count2():
  delta = today - datetime.strptime(start_marry_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  birth = ZhDate(date.today().year, int(birthday_m), int(birthday_d)).to_datetime()
  if birth < datetime.strptime(datetime.now().strftime('%Y-%m-%d'),"%Y-%m-%d"):
    birth = ZhDate(date.today().year + 1, int(birthday_m), int(birthday_d)).to_datetime()
  diff = birth.toordinal() - today.toordinal()
  if diff == 0:
    return {"value":"今天是你的生日~ 生日快乐","color":"#FA9F4E"}
  return {"value":"距离你的生日还有 " + str(diff) + "天"}

def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.strptime(datetime.now().strftime('%Y-%m-%d'),"%Y-%m-%d"):
    next = next.replace(year=next.year + 1)
  diff = next.toordinal() - today.toordinal()
  if diff == 0:
    return {"value":"今天是小刘的生日~ 祝他生日快乐","color":"#FA9F4E"}
  return {"value":"距离小刘的生日还有 " + str(diff) + "天"}


def get_marry_left():
  next = datetime.strptime(str(date.today().year) + "-" + marry, "%Y-%m-%d")
  if next < datetime.strptime(datetime.now().strftime('%Y-%m-%d'),"%Y-%m-%d"):
    next = next.replace(year=next.year + 1)
  diff = next.toordinal() - today.toordinal()
  if diff == 0:
    return {"value":"今天是我们两个的结婚纪念日~ 庆祝一下吧","color":"#FA9F4E"}
  return {"value":"距离我们的结婚纪念日还有 " + str(diff) + "天"}

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
data = {"today":{"value":datetime.now().strftime('%Y-%m-%d'),"color":"#87CEEB"},"weather_words":{"value":weather_words,"color":weather_words_color} ,"weather":{"value":weather},"temp_low":{"value":str(temp_low) + '℃',"color":temp_low_color},"temp_high":{"value":str(temp_high) + '℃',"color":temp_high_color},"next_words":{"value":"每一天都值得铭记↓","color":"#FFB6C1"},"next_words2":{"value":"余生有幸和你在一起","color":"#FFB6C1"},"love_days":{"value":get_count()},"marry_days":{"value":get_count2()},"birthday_left":get_birthday(),"birthday_left2":get_birthday2(),"marry_left":get_marry_left(),"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
