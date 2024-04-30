import avg_recent_price

# json_data = {'RESULT': {'OIL': [{'DATE': '20240422', 'PRODCD': 'B027', 'PRICE': 1707.25}, {'DATE': '20240422', 'PRODCD': 'B034', 'PRICE': 1950.18}, {'DATE': '20240422', 'PRODCD': 'C004', 'PRICE': 1369.09}, {'DATE': '20240422', 'PRODCD': 'D047', 'PRICE': 1566.71}, {'DATE': '20240422', 'PRODCD': 'K015', 'PRICE': 970.01}, {'DATE': '20240423', 'PRODCD': 'B027', 'PRICE': 1708.08}, {'DATE': '20240423', 'PRODCD': 'B034', 'PRICE': 1950.47}, {'DATE': '20240423', 'PRODCD': 'C004', 'PRICE': 1369.25}, {'DATE': '20240423', 'PRODCD': 'D047', 'PRICE': 1566.58}, {'DATE': '20240423', 'PRODCD': 'K015', 'PRICE': 969.88}, {'DATE': '20240424', 'PRODCD': 'B027', 'PRICE': 1709.56}, {'DATE': '20240424', 'PRODCD': 'B034', 'PRICE': 1950.6}, {'DATE': '20240424', 'PRODCD': 'C004', 'PRICE': 1369.17}, {'DATE': '20240424', 'PRODCD': 'D047', 'PRICE': 1566.85}, {'DATE': '20240424', 'PRODCD': 'K015', 'PRICE': 970.11}, {'DATE': '20240425', 'PRODCD': 'B027', 'PRICE': 1710.47}, {'DATE': '20240425', 'PRODCD': 'B034', 'PRICE': 1952.42}, {'DATE': '20240425', 'PRODCD': 'C004', 'PRICE': 1369.16}, {'DATE': '20240425', 'PRODCD': 'D047', 'PRICE': 1566.9}, {'DATE': '20240425', 'PRODCD': 'K015', 'PRICE': 969.88}, {'DATE': '20240426', 'PRODCD': 'B027', 'PRICE': 1711.28}, {'DATE': '20240426', 'PRODCD': 'B034', 'PRICE': 1953.17}, {'DATE': '20240426', 'PRODCD': 'C004', 'PRICE': 1369.07}, {'DATE': '20240426', 'PRODCD': 'D047', 'PRICE': 1566.87}, {'DATE': '20240426', 'PRODCD': 'K015', 'PRICE': 969.87}, {'DATE': '20240427', 'PRODCD': 'B027', 'PRICE': 1711.59}, {'DATE': '20240427', 'PRODCD': 'B034', 'PRICE': 1952.8}, {'DATE': '20240427', 'PRODCD': 'C004', 'PRICE': 1368.78}, {'DATE': '20240427', 'PRODCD': 'D047', 'PRICE': 1566.52}, {'DATE': '20240427', 'PRODCD': 'K015', 'PRICE': 970.07}, {'DATE': '20240428', 'PRODCD': 'B027', 'PRICE': 1711.94}, {'DATE': '20240428', 'PRODCD': 'B034', 'PRICE': 1953.09}, {'DATE': '20240428', 'PRODCD': 'C004', 'PRICE': 1368.71}, {'DATE': '20240428', 'PRODCD': 'D047', 'PRICE': 1566.42}, {'DATE': '20240428', 'PRODCD': 'K015', 'PRICE': 970.01}]}}
#
# gasoline_whole_price = json_data['RESULT']['OIL'][30]['PRICE']
# print(gasoline_whole_price)
# diesel_whole_price = json_data['RESULT']['OIL'][33]['PRICE']
# print(diesel_whole_price)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Oil Prices Graph")

        # 버튼 생성
        self.plot_button = QPushButton('휘발유 및 경유 평균 가격 조회')
        self.plot_button.clicked.connect(self.show_prices)


        # 중앙 위젯 및 레이아웃 생성
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.plot_button)

        # 초기에 한번 실행하여 버튼 텍스트 설정
        self.show_prices()

    def show_prices(self):
        # 주어진 JSON 데이터
        json_data = {'RESULT': {'OIL': [{'DATE': '20240422', 'PRODCD': 'B027', 'PRICE': 1707.25}, {'DATE': '20240422', 'PRODCD': 'B034', 'PRICE': 1950.18}, {'DATE': '20240422', 'PRODCD': 'C004', 'PRICE': 1369.09}, {'DATE': '20240422', 'PRODCD': 'D047', 'PRICE': 1566.71}, {'DATE': '20240422', 'PRODCD': 'K015', 'PRICE': 970.01}, {'DATE': '20240423', 'PRODCD': 'B027', 'PRICE': 1708.08}, {'DATE': '20240423', 'PRODCD': 'B034', 'PRICE': 1950.47}, {'DATE': '20240423', 'PRODCD': 'C004', 'PRICE': 1369.25}, {'DATE': '20240423', 'PRODCD': 'D047', 'PRICE': 1566.58}, {'DATE': '20240423', 'PRODCD': 'K015', 'PRICE': 969.88}, {'DATE': '20240424', 'PRODCD': 'B027', 'PRICE': 1709.56}, {'DATE': '20240424', 'PRODCD': 'B034', 'PRICE': 1950.6}, {'DATE': '20240424', 'PRODCD': 'C004', 'PRICE': 1369.17}, {'DATE': '20240424', 'PRODCD': 'D047', 'PRICE': 1566.85}, {'DATE': '20240424', 'PRODCD': 'K015', 'PRICE': 970.11}, {'DATE': '20240425', 'PRODCD': 'B027', 'PRICE': 1710.47}, {'DATE': '20240425', 'PRODCD': 'B034', 'PRICE': 1952.42}, {'DATE': '20240425', 'PRODCD': 'C004', 'PRICE': 1369.16}, {'DATE': '20240425', 'PRODCD': 'D047', 'PRICE': 1566.9}, {'DATE': '20240425', 'PRODCD': 'K015', 'PRICE': 969.88}, {'DATE': '20240426', 'PRODCD': 'B027', 'PRICE': 1711.28}, {'DATE': '20240426', 'PRODCD': 'B034', 'PRICE': 1953.17}, {'DATE': '20240426', 'PRODCD': 'C004', 'PRICE': 1369.07}, {'DATE': '20240426', 'PRODCD': 'D047', 'PRICE': 1566.87}, {'DATE': '20240426', 'PRODCD': 'K015', 'PRICE': 969.87}, {'DATE': '20240427', 'PRODCD': 'B027', 'PRICE': 1711.59}, {'DATE': '20240427', 'PRODCD': 'B034', 'PRICE': 1952.8}, {'DATE': '20240427', 'PRODCD': 'C004', 'PRICE': 1368.78}, {'DATE': '20240427', 'PRODCD': 'D047', 'PRICE': 1566.52}, {'DATE': '20240427', 'PRODCD': 'K015', 'PRICE': 970.07}, {'DATE': '20240428', 'PRODCD': 'B027', 'PRICE': 1711.94}, {'DATE': '20240428', 'PRODCD': 'B034', 'PRICE': 1953.09}, {'DATE': '20240428', 'PRODCD': 'C004', 'PRICE': 1368.71}, {'DATE': '20240428', 'PRODCD': 'D047', 'PRICE': 1566.42}, {'DATE': '20240428', 'PRODCD': 'K015', 'PRICE': 970.01}]}}

        gasoline_whole_price = json_data['RESULT']['OIL'][30]['PRICE']
        diesel_whole_price = json_data['RESULT']['OIL'][33]['PRICE']

        self.plot_button.setText("전국 휘발유 평균 가격: {:.2f}원\n  전국 경   유 평균 가격: {:.2f}원  ".format(gasoline_whole_price, diesel_whole_price))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
