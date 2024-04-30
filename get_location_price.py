import requests
from pyproj import Transformer

def location(): #find users location
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyD_F2udUu_fQDG64_BSMDUlPrgxODTQ9r4'
    data = {
        'considerIp': True,
        #'homeMobileCountryCode': 450,
        #'homeMobileNetworkCode': 5,
        #'radioType':'gsm',
        #'carrier': "SKTelecom",
        #"wifiAccessPoints":[{'macAddress':'40:DC:9D:06:EC:CA'}]
    }
    result = requests.post(url, data)
    a=result.json()
    lat=a['location']['lat'] # Y point
    lng=a['location']['lng'] # X point
    return lat,lng

def ask_oil_type(ans):
    if ans == "경유" :
        return "D047"
    elif ans == "휘발유" :
        return "B027"
    else :
        return None

def browse(x_point,y_point,oil_type):
    url = 'http://www.opinet.co.kr/api/aroundAll.do'
    payload = {
        "code" : 'F240425132', # 인증키 값은 오피넷에 메일을 보내 받을 수 있음
        "out" : "json",
        "x" : x_point,
        "y" : y_point,
        "radius" : "5000",
        "prodcd" : oil_type ,
        "sort" : "1"
        }
    result = requests.get(url,params=payload).json()
    return result

def wgs84_to_katec(wgs84_x, wgs84_y):
    # WGS84 좌표계와 KATEC 좌표계를 정의합니다.
    transformer = Transformer.from_crs("epsg:4326", "epsg:5178")

    # WGS84 좌표를 KATEC 좌표로 변환합니다.
    katec_x, katec_y = transformer.transform(wgs84_x, wgs84_y)

    return katec_y, katec_x

x, y =location()
tx, ty =wgs84_to_katec(x, y)
print(x,y)
print(tx,ty)
print(browse(tx, ty , 'B027'))