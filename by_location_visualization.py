import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


def plot_interactive_graph():
    fig = make_subplots(rows=1, cols=1)
    data = requests.get('https://www.opinet.co.kr/api/avgSidoPrice.do', params={"code" : "F240425132","out" : "json"}).json()

    all_sido_names = [item['SIDONM'] for item in data['RESULT']['OIL']]
    gasoline_data = {item['SIDONM']: item['PRICE'] for item in data['RESULT']['OIL'] if item['PRODCD'] == 'B027'}
    diesel_data = {item['SIDONM']: item['PRICE'] for item in data['RESULT']['OIL'] if item['PRODCD'] == 'D047'}

    for sido_name, price in gasoline_data.items():
        fig.add_trace(go.Scatter(x=[sido_name], y=[price], mode='markers', marker=dict(color='red'), name=sido_name+'(휘발유)'), row=1, col=1)
    for sido_name, price in diesel_data.items():
        fig.add_trace(go.Scatter(x=[sido_name], y=[price], mode='markers', marker=dict(color='blue'), name=sido_name+'(경   유)'), row=1, col=1)

    fig.update_xaxes(title_text="지역", row=1, col=1)
    fig.update_yaxes(title_text="가격 (원)", row=1, col=1)
    fig.update_layout(title='전국 평균 유가(지역별)')

    return fig

def generate_html(fig):
    html = pio.to_html(fig, include_plotlyjs='cdn')
    return html

# 예시 코드
if __name__ == "__main__":
    fig = plot_interactive_graph()
    html = generate_html(fig)
    print(html)  # HTML 코드를 다른 파일에서 사용할 수 있도록 반환합니다.