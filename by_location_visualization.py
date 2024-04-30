import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton, QVBoxLayout, QWidget
import plotly.graph_objects as go
import requests

class OilPriceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oil Prices App")

        # 라디오 버튼 생성
        self.gasoline_radio = QRadioButton('휘발유')
        self.gasoline_radio.toggled.connect(self.plot_avg_prices)
        self.diesel_radio = QRadioButton('경유')
        self.diesel_radio.toggled.connect(self.plot_avg_prices)
        self.gasoline_and_diesel_radio = QRadioButton('휘발유 + 경유')
        self.gasoline_and_diesel_radio.toggled.connect(self.plot_both_prices)

        # 중앙 위젯 및 레이아웃 생성
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.gasoline_radio)
        layout.addWidget(self.diesel_radio)
        layout.addWidget(self.gasoline_and_diesel_radio)

    def plot_avg_prices(self, checked):
        if checked:
            if self.sender() == self.gasoline_radio:
                product_code = 'B027'  # 휘발유 코드
                product_name = '휘발유'
                line_color = 'red'  # 휘발유 선 색상을 빨간색으로 설정
            elif self.sender() == self.diesel_radio:
                product_code = 'D047'  # 경유 코드
                product_name = '경유'
                line_color = 'blue'  # 경유 선 색상을 파란색으로 설정

            # 주어진 JSON 데이터
            data = self.avg_sido_price()

            # 선택된 유종의 데이터만 선택
            selected_data = [item for item in data['RESULT']['OIL'] if item['PRODCD'] == product_code]

            # 유종의 가격 데이터 추출
            prices = [item['PRICE'] for item in selected_data]
            sido_names = [item['SIDONM'] for item in selected_data]

            # 그래프 그리기
            self.plot_graph(prices, sido_names=sido_names, product_name=product_name, line_color=line_color)

    def avg_sido_price(self):
        url = 'https://www.opinet.co.kr/api/avgSidoPrice.do'
        payload = {
            "code": "F240425132",
            "out": "json",
        }
        result = requests.get(url, params=payload).json()
        return result

    def plot_both_prices(self, checked):
        if checked:
            # 주어진 JSON 데이터
            data = self.avg_sido_price()

            # 휘발유와 경유 데이터 추출
            gasoline_data = [item for item in data['RESULT']['OIL'] if item['PRODCD'] == 'B027']
            diesel_data = [item for item in data['RESULT']['OIL'] if item['PRODCD'] == 'D047']

            # 휘발유와 경유의 가격 데이터 추출
            gasoline_prices = [item['PRICE'] for item in gasoline_data]
            diesel_prices = [item['PRICE'] for item in diesel_data]
            sido_names = [item['SIDONM'] for item in gasoline_data]

            # 그래프 그리기
            self.plot_graph(gasoline_prices, diesel_prices, sido_names, '휘발유 + 경유')

    def plot_graph(self, prices1, prices2=None, sido_names=None, product_name=None, line_color='blue'):
        # 그래프 생성
        fig = go.Figure()

        if prices2 is not None and sido_names is not None:
            fig.add_trace(go.Scatter(x=sido_names, y=prices1, mode='lines+markers', name='휘발유', marker=dict(color='red')))
            fig.add_trace(go.Scatter(x=sido_names, y=prices2, mode='lines+markers', name='경유', marker=dict(color='blue')))
        else:
            if sido_names is None:
                sido_names = ['']*len(prices1)  # 빈 문자열 리스트로 초기화
            fig.add_trace(go.Scatter(x=sido_names, y=prices1, mode='lines+markers', name=product_name, marker=dict(color=line_color)))

        fig.update_layout(title=f'지역별 평균 가격 ({product_name})', xaxis_title='지역', yaxis_title='가격 (원)')
        fig.show()

def main():
    app = QApplication(sys.argv)
    window = OilPriceApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()