import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QComboBox, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots
import plotly.io as pio

class OilPriceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Oil Prices App")

        # 중앙 위젯 및 레이아웃 생성
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # 버튼 생성
        self.button_gasoline = QPushButton("휘발유")
        self.button_gasoline.clicked.connect(self.update_graph)
        layout.addWidget(self.button_gasoline)

        self.button_diesel = QPushButton("경유")
        self.button_diesel.clicked.connect(self.update_graph)
        layout.addWidget(self.button_diesel)

        self.button_both = QPushButton("휘발유+경유")
        self.button_both.clicked.connect(self.update_graph)
        layout.addWidget(self.button_both)

        # 그래프 생성 및 추가
        fig = make_subplots(rows=1, cols=1)
        self.plot_interactive_graph(fig)
        html = pio.to_html(fig, include_plotlyjs='cdn')
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html)
        layout.addWidget(self.web_view)

    def avg_sido_price(self):
        url = 'https://www.opinet.co.kr/api/avgSidoPrice.do'
        payload = {
            "code": "F240425132",
            "out": "json",
        }
        result = requests.get(url, params=payload).json()
        return result

    def plot_interactive_graph(self, fig):
        # 주어진 JSON 데이터
        data = self.avg_sido_price()

        # 모든 지역 이름 추출
        all_sido_names = [item['SIDONM'] for item in data['RESULT']['OIL']]

        # 휘발유와 경유 데이터 추출
        gasoline_data = {sido: None for sido in all_sido_names}
        diesel_data = {sido: None for sido in all_sido_names}
        for item in data['RESULT']['OIL']:
            if item['PRODCD'] == 'B027':
                gasoline_data[item['SIDONM']] = item['PRICE']
            elif item['PRODCD'] == 'D047':
                diesel_data[item['SIDONM']] = item['PRICE']

        # 그래프 그리기
        for sido_name in all_sido_names:
            if sido_name in gasoline_data:
                fig.add_trace(go.Scatter(x=[sido_name], y=[gasoline_data[sido_name]], mode='markers', marker=dict(color='red'), name='휘발유'), row=1, col=1)
            if sido_name in diesel_data:
                fig.add_trace(go.Scatter(x=[sido_name], y=[diesel_data[sido_name]], mode='markers', marker=dict(color='blue'), name='경유'), row=1, col=1)

        fig.update_xaxes(title_text="지역", row=1, col=1)
        fig.update_yaxes(title_text="가격 (원)", row=1, col=1)

    def update_graph(self):
        selected_region = "" # 이 부분은 삭제됩니다.

        # 주어진 JSON 데이터
        data = self.avg_sido_price()

        # 모든 지역 이름 추출
        all_sido_names = [item['SIDONM'] for item in data['RESULT']['OIL']]

        # 특정 지역의 휘발유와 경유 데이터 추출
        gasoline_data = {item['SIDONM']: item['PRICE'] for item in data['RESULT']['OIL'] if item['PRODCD'] == 'B027'}
        diesel_data = {item['SIDONM']: item['PRICE'] for item in data['RESULT']['OIL'] if item['PRODCD'] == 'D047'}

        # 선택된 버튼에 따라서 그래프 데이터 선택
        fig = make_subplots(rows=1, cols=1)
        if self.sender() == self.button_gasoline or self.sender() == self.button_both:
            for sido_name, price in gasoline_data.items():
                fig.add_trace(go.Scatter(x=[sido_name], y=[price], mode='markers', marker=dict(color='red'), name='휘발유'), row=1, col=1)
        if self.sender() == self.button_diesel or self.sender() == self.button_both:
            for sido_name, price in diesel_data.items():
                fig.add_trace(go.Scatter(x=[sido_name], y=[price], mode='markers', marker=dict(color='blue'), name='경유'), row=1, col=1)

        fig.update_xaxes(title_text="지역", row=1, col=1)
        fig.update_yaxes(title_text="가격 (원)", row=1, col=1)

        html = pio.to_html(fig, include_plotlyjs='cdn')
        self.web_view.setHtml(html)

def main():
    app = QApplication(sys.argv)
    window = OilPriceApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
