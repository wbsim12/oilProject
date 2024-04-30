import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oil Prices")

        # 중앙 위젯 및 레이아웃 생성
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # 전국 주유소 평균 가격 라벨
        self.all_price_label = QLabel("               전국 평균 ")
        layout.addWidget(self.all_price_label)

        # 휘발유와 경유의 가격을 표시할 라벨들
        self.all_gasoline_label = QLabel()
        self.all_diesel_label = QLabel()
        layout.addWidget(self.all_gasoline_label)
        layout.addWidget(self.all_diesel_label)

        # 경기도 성남시 주유소 평균 가격 라벨
        self.local_price_label = QLabel("\n              성남시 평균")
        layout.addWidget(self.local_price_label)

        # 휘발유와 경유의 가격을 표시할 라벨들
        self.local_gasoline_label = QLabel()
        self.local_diesel_label = QLabel()
        layout.addWidget(self.local_gasoline_label)
        layout.addWidget(self.local_diesel_label)

        # 초기에 한번 실행하여 텍스트 설정
        self.show_prices()

    def show_prices(self):
        # API를 통해 전국 주유소와 경기도 성남시 주유소의 평균 가격 가져오기
        all_gasoline_data, all_diesel_data = fetch_prices()
        local_gasoline_data, local_diesel_data = fetch_local_prices()

        # 전국 평균 가격과 DIFF 정보 설정
        all_gasoline_price = float(all_gasoline_data['PRICE'])
        all_gasoline_diff = float(all_gasoline_data['DIFF'])
        all_diesel_price = float(all_diesel_data['PRICE'])
        all_diesel_diff = float(all_diesel_data['DIFF'])

        # 경기도 성남시 평균 가격과 DIFF 정보 설정
        local_gasoline_price = float(local_gasoline_data['PRICE'])
        local_gasoline_diff = float(local_gasoline_data['DIFF'])
        local_diesel_price = float(local_diesel_data['PRICE'])
        local_diesel_diff = float(local_diesel_data['DIFF'])

        # 각각의 라벨에 평균 가격과 DIFF 정보 설정
        self.all_gasoline_label.setText("휘발유 {:.2f}원 (전일대비 {:+.2f}원)".format(all_gasoline_price, all_gasoline_diff))
        self.all_diesel_label.setText("경유 {:.2f}원 (전일대비 {:+.2f}원)".format(all_diesel_price, all_diesel_diff))
        self.local_gasoline_label.setText("휘발유 {:.2f}원 (전일대비 {:+.2f}원)".format(local_gasoline_price, local_gasoline_diff))
        self.local_diesel_label.setText("경유 {:.2f}원 (전일대비 {:+.2f}원)".format(local_diesel_price, local_diesel_diff))

def fetch_prices():
    # 오피넷 API를 통해 전국 주유소의 평균 가격 가져오기
    url = 'http://www.opinet.co.kr/api/avgAllPrice.do'
    payload = {
        "code": 'F240425132',  # 인증키 값은 오피넷에 메일을 보내 받을 수 있음
        "out": "json"
    }
    result = requests.get(url, params=payload).json()

    # 휘발유와 경유의 데이터 추출
    all_gasoline_data = None
    all_diesel_data = None
    for item in result['RESULT']['OIL']:
        if item['PRODCD'] == 'B027':  # 휘발유 코드
            all_gasoline_data = item
        elif item['PRODCD'] == 'D047':  # 경유 코드
            all_diesel_data = item

    return all_gasoline_data, all_diesel_data

def fetch_local_prices():
    # 오피넷 API를 통해 경기도 성남시 주유소의 평균 가격 가져오기
    url = 'http://www.opinet.co.kr/api/avgSigunPrice.do'
    payload = {
        "code": 'F240425132',  # 인증키 값은 오피넷에 메일을 보내 받을 수 있음
        "out": "json",
        "sido": '02',  # 경기도 코드
        "sigun": '0202'  # 성남시 코드
    }
    result = requests.get(url, params=payload).json()

    # 휘발유와 경유의 데이터 추출
    local_gasoline_data = None
    local_diesel_data = None
    for item in result['RESULT']['OIL']:
        if item['PRODCD'] == 'B027':  # 휘발유 코드
            local_gasoline_data = item
        elif item['PRODCD'] == 'D047':  # 경유 코드
            local_diesel_data = item

    return local_gasoline_data, local_diesel_data

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
