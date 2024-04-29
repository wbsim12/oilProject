import requests
import json
from pyproj import Proj
from pyproj import transform

def ask_oil_type(ans):
    if ans == "자동차경유":
        return "D047"
    elif ans == "보통휘발유":
        return "B027"
    elif ans == "B034":
        return "고급휘발유"
    elif ans == "C004":
        return "실내등유"
    elif ans == "K015":
        return "자동차부탄"
    else :
        return None

def code_to_name(ans):
    if ans == "D047" :
        return "자동차경유"
    elif ans == "B027" :
        return "보통휘발유"
    elif ans == "B034" :
        return "고급휘발유"
    elif ans == "C004" :
        return "실내등유"
    elif ans == "K015" :
        return "자동차부탄"
    else :
        return None

def avg_sido_price():
    url = 'https://www.opinet.co.kr/api/avgSidoPrice.do'
    payload = {
        "code" : "F240425132",
        "out" : "json",
        }
    result = requests.get(url,params=payload).json()
    return result

def prnt_avg_price(json_value):
    for i in range(len(json_value['RESULT']['OIL'])):
       print(json_value['RESULT']['OIL'][i]['SIDONM'], code_to_name(json_value['RESULT']['OIL'][i]['PRODCD']),
         f"평균 가격은 {json_value['RESULT']['OIL'][i]['PRICE']}")

#json_value = avg_sido_price() #전국평균가격을 받아옴, 지역별 평균 가격을 받아옴
#prnt_avg_price(json_value)

def avg_recent_price():
    url = 'https://www.opinet.co.kr/api/avgRecentPrice.do'
    payload = {
        "code" : "F240425132",
        "out" : "json",
        }
    result = requests.get(url,params=payload).json()
    return result

def prnt_avg_recent_price(json_value):
    for i in range(len(json_value['RESULT']['OIL'])):
       print(json_value['RESULT']['OIL'][i]['SIDONM'], code_to_name(json_value['RESULT']['OIL'][i]['PRODCD']),
         f"평균 가격은 {json_value['RESULT']['OIL'][i]['PRICE']}")

json_value = avg_recent_price()  #7일간의 가격을 받아옴
prnt_avg_recent_price(json_value['RESULT']['OIL'])

