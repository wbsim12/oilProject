import plotly.graph_objects as go
import requests

def avg_sido_price():
    url = 'https://www.opinet.co.kr/api/avgSidoPrice.do'
    payload = {
        "code" : "F240425132",
        "out" : "json",
    }
    result = requests.get(url,params=payload).json()
    return result

# 주어진 JSON 데이터
data = avg_sido_price()

# 휘발유와 경유의 데이터만 선택
selected_data = [item for item in data['RESULT']['OIL'] if item['PRODCD'] in ['B027', 'B034']]

# 휘발유와 경유의 가격 데이터 추출
gasoline_prices = [item['PRICE'] for item in selected_data if item['PRODCD'] == 'B027']
diesel_prices = [item['PRICE'] for item in selected_data if item['PRODCD'] == 'B034']
sido_names = [item['SIDONM'] for item in selected_data if item['PRODCD'] == 'B027']  # SIDONM 데이터 추출

# 최저 및 최고 가격 및 위치 찾기
min_gasoline_price = min(gasoline_prices)
max_gasoline_price = max(gasoline_prices)
min_gasoline_location = sido_names[gasoline_prices.index(min_gasoline_price)]
max_gasoline_location = sido_names[gasoline_prices.index(max_gasoline_price)]

min_diesel_price = min(diesel_prices)
max_diesel_price = max(diesel_prices)
min_diesel_location = sido_names[diesel_prices.index(min_diesel_price)]
max_diesel_location = sido_names[diesel_prices.index(max_diesel_price)]

# 그래프 생성
fig = go.Figure()
fig.add_trace(go.Scatter(x=sido_names, y=gasoline_prices, mode='lines+markers', name='경유', marker=dict(color='blue')))
fig.add_trace(go.Scatter(x=sido_names, y=diesel_prices, mode='lines+markers', name='휘발유', marker=dict(color='red')))

# 휘발유 최저 및 최고 가격 마킹
fig.add_trace(go.Scatter(x=[min_gasoline_location], y=[min_gasoline_price], mode='markers', name='경유 최저가', marker=dict(color='yellow', size=10)))
fig.add_trace(go.Scatter(x=[max_gasoline_location], y=[max_gasoline_price], mode='markers', name='경유 최고가', marker=dict(color='purple', size=10)))

# 경유 최저 및 최고 가격 마킹
fig.add_trace(go.Scatter(x=[min_diesel_location], y=[min_diesel_price], mode='markers', name='휘발유 최저가', marker=dict(color='yellow', size=10)))
fig.add_trace(go.Scatter(x=[max_diesel_location], y=[max_diesel_price], mode='markers', name='휘발유 최고가', marker=dict(color='purple', size=10)))

# 그래프 레이아웃 설정
fig.update_layout(title='지역별 휘발유 및 경유 가격', xaxis_title='지역', yaxis_title='가격 (원)')

# 그래프 출력
fig.show()
