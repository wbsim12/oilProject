import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import json
import plotly.graph_objects as go
class avg_price():

    # def avg_recent_price(self):
    #     url = 'https://www.opinet.co.kr/api/avgRecentPrice.do'
    #     payload = {
    #         "code" : "F240425132",
    #         "out" : "json",
    #         }
    #     result = requests.get(url,params=payload).json()
    #     return result

    def plot_graph(self):
            # 주어진 JSON 데이터
        #json_data = self.avg_recent_price()
        json_data = requests.get('https://www.opinet.co.kr/api/avgRecentPrice.do', params={"code" : "F240425132","out" : "json"}).json()

        if json_data:
                # 데이터 추출
            oil_data = json_data['RESULT']['OIL']

                # 경유와 휘발유 가격 추출
            diesel_prices = [entry['PRICE'] for entry in oil_data if entry['PRODCD'] == 'D047']
            gasoline_prices = [entry['PRICE'] for entry in oil_data if entry['PRODCD'] == 'B027']
            dates = [entry['DATE'] for entry in oil_data if entry['PRODCD'] == 'D047']  # 날짜는 경유의 경우에만 필요

                # 그래프 생성
            fig = go.Figure()

                # 경유 그래프 추가
            fig.add_trace(go.Scatter(x=dates, y=diesel_prices, mode='lines+markers', name='경유', marker=dict(color='blue')))

                # 휘발유 그래프 추가
            fig.add_trace(go.Scatter(x=dates, y=gasoline_prices, mode='lines+markers', name='휘발유', marker=dict(color='red')))

                # 그래프 레이아웃 설정
            fig.update_layout(title='Oil Prices Graph', xaxis_title='날짜', yaxis_title='가격 (원)')

                # 그래프 출력
            return fig


#class MainWindow(QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #
    #     self.setWindowTitle("Oil Prices Graph")
    #
    #     # 버튼 생성
    #     self.plot_button = QPushButton('그래프 그리기')
    #     self.plot_button.clicked.connect(self.plot_graph)
    #
    #     # 중앙 위젯 및 레이아웃 생성
    #     self.central_widget = QWidget()
    #     self.setCentralWidget(self.central_widget)
    #     layout = QVBoxLayout(self.central_widget)
    #     layout.addWidget(self.plot_button)

    # def plot_graph(self):
    #     # 주어진 JSON 데이터
    #     json_data = avg_recent_price()
    #
    #     if json_data:
    #         # 데이터 추출
    #         oil_data = json_data['RESULT']['OIL']
    #
    #         # 경유와 휘발유 가격 추출
    #         diesel_prices = [entry['PRICE'] for entry in oil_data if entry['PRODCD'] == 'D047']
    #         gasoline_prices = [entry['PRICE'] for entry in oil_data if entry['PRODCD'] == 'B027']
    #         dates = [entry['DATE'] for entry in oil_data if entry['PRODCD'] == 'D047']  # 날짜는 경유의 경우에만 필요
    #
    #         # 그래프 생성
    #         fig = go.Figure()
    #
    #         # 경유 그래프 추가
    #         fig.add_trace(go.Scatter(x=dates, y=diesel_prices, mode='lines+markers', name='경유', marker=dict(color='blue')))
    #
    #         # 휘발유 그래프 추가
    #         fig.add_trace(go.Scatter(x=dates, y=gasoline_prices, mode='lines+markers', name='휘발유', marker=dict(color='red')))
    #
    #         # 그래프 레이아웃 설정
    #         fig.update_layout(title='Oil Prices Graph', xaxis_title='날짜', yaxis_title='가격 (원)')
    #
    #         # 그래프 출력
    #         fig.show()

# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())
#
# if __name__ == "__main__":
#     main()