import requests
import json

def ask_oil_type(ans):
    if ans == "자동차경유":
        return "D047"
    elif ans == "보통휘발유":
        return "B027"
    else :
        return None

def code_to_name(ans):
    if ans == "D047" :
        return "자동차경유"
    elif ans == "B027" :
        return "보통휘발유"
    else :
        return None

# def ask_oil_type(ans):
#     if ans == "자동차경유":
#         return "D047"
#     elif ans == "보통휘발유":
#         return "B027"
#     elif ans == "고급휘발유":
#         return "B034"
#     elif ans == "실내등유":
#         return "C004"
#     elif ans == "자동차부탄":
#         return "K015"
#     else :
#         return None


# def code_to_name(ans):
#     if ans == "D047" :
#         return "자동차경유"
#     elif ans == "B027" :
#         return "보통휘발유"
#     elif ans == "B034" :
#         return "고급휘발유"
#     elif ans == "C004" :
#         return "실내등유"
#     elif ans == "K015" :
#         return "자동차부탄"
#     else :
#         return None

def avg_sido_price():
    url = 'https://www.opinet.co.kr/api/avgSidoPrice.do'
    payload = {
        "code" : "F240425132",
        "out" : "json",
        }
    result = requests.get(url,params=payload).json()
    return result

def get_diesel_price(json_value):
    for i in range(len(json_value['RESULT']['OIL'])):
        if(json_value['RESULT']['OIL'][i]['PRODCD'] ==('D047')):
            print(json_value['RESULT']['OIL'][i]['SIDONM'], code_to_name(json_value['RESULT']['OIL'][i]['PRODCD']),
            f"평균 가격은 {json_value['RESULT']['OIL'][i]['PRICE']}")


def get_gasoline_price(json_value):
    for i in range(len(json_value['RESULT']['OIL'])):
        if(json_value['RESULT']['OIL'][i]['PRODCD'] ==('B027')):
            print(json_value['RESULT']['OIL'][i]['SIDONM'], code_to_name(json_value['RESULT']['OIL'][i]['PRODCD']),
            f"평균 가격은 {json_value['RESULT']['OIL'][i]['PRICE']}")

json_value = avg_sido_price() #전국평균가격을 받아옴, 지역별 평균 가격을 받아옴
print(json_value)
#get_diesel_price(json_value)
#get_gasoline_price(json_value)

