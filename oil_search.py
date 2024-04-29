import requests
import os, sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication

root = os.path.dirname(os.path.abspath(__file__))

MainUI = uic.loadUiType(os.path.join(root, 'testMain.ui'))[0]



class MainDialog(QMainWindow, MainUI):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("확인 테스트")
        self.label.setGeometry(0, 0, 640, 480)
        #self.address_to_coords()
        self.lineEdit.setPlaceholderText('검색 장소 입력 체크')
        check_test = self.address_to_coords()


        map_image = self.get_static_map(check_test[0], check_test[1])

        pixmap = QPixmap()
        pixmap.loadFromData(map_image)
        self.label.setPixmap(pixmap)
        # 예시 주소로 좌표 변환
        #address = "경기도 성남시 분당구 삼평동 681"

        print(check_test, type(check_test))
        print(check_test[0])
        print(check_test[1])


    def address_to_coords(self):
        address = "경기도 성남시 분당구 삼평동 681"
        base_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
        client_id = "7ddepf4bxh"
        client_secret = "QhXyiYlQ5OxeLV7Oar0CH6UptIOtaqN7RH8cps2y"

        params = {
            "query": address
        }

        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret
        }

        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                coords = data['addresses'][0]['x'], data['addresses'][0]['y']
                print("x 내용 확인" + data['addresses'][0]['x'])
                print("y 내용 확인" + data['addresses'][0]['y'])
                return coords
            else:
                print("Error:", data['status'])
                return None
        else:
            print("Error:", response.status_code)
            return None



    def get_static_map(self, lon, lat):

        base_url = "https://naveropenapi.apigw.ntruss.com/map-static/v2/raster"
        client_id = "7ddepf4bxh"
        client_secret = "QhXyiYlQ5OxeLV7Oar0CH6UptIOtaqN7RH8cps2y"
        zoom = 16
        width = 640
        height = 480

        params = {
            "center": f"{lon},{lat}",  # 중심 좌표 설정
            "level": zoom,
            "w": width,
            "h": height
        }

        headers = {
            "X-NCP-APIGW-API-KEY-ID": client_id,
            "X-NCP-APIGW-API-KEY": client_secret
        }

        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            return response.content
        else:
            print("Error:", response.status_code)
            return None





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())
