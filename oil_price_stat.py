import os
import pandas as pd
import traceback
import time
from datetime import datetime, timedelta

import selenium.common.exceptions
from PyQt5 import uic
from PyQt5.QtWidgets import *

from selenium import webdriver  # pip install selenium==4.8 -> pip3 install -U selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
root = os.path.dirname(os.path.abspath(__file__))
stat_UI = uic.loadUiType(os.path.join(root, './ui/oil_stat.ui'))[0]


def select_attr(df, attr, val):  # 해당 속성의 값들만 골라내고 그 속성은 drop한다.
    return df[df[attr] == val].drop(attr, axis=1)


def mod_date_num(df):
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')
    city_names = list(df.columns[2:])
    for city in city_names:
        df[city] = df[city].str.replace(',', '').astype(float)


def get_previous_date(days):
    return datetime.today() - timedelta(days=days)


def make_2d_table(datas):
    data_rows = []
    for row in datas:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text for cell in cells]  # 주의!
        data_rows.append(row_data)
    return data_rows


def find_max_min_avg(df):
    ret_max = -1
    ret_min = 10000

    city_list = df.head(1)
    for city in city_list:
        if city == '날짜':
            continue
        max_temp = df[city].max()
        min_temp = df[city].min()
        if ret_max < max_temp:
            ret_max = max_temp
        if ret_min > min_temp:
            ret_min = min_temp
    return ret_max, ret_min


def draw_axis(df):    
    max_now, min_now = find_max_min_avg(df)
    plt.ylim(int(min_now) - 10, int(max_now) + 10)
    # plt.yticks(range(int(min_now - 50), int(max_now + 50), 50))  # range 함수로 전달하면 소수점으로 표기됨.
    plt.yticks(range(int(min_now - 10), int(max_now + 11)))  # ylim과 똑같은 범위로 전달
    # 이렇게 작성해도 10 보다 작은 범위에 그래프가 그려지는 경우 소수점이 표기된다.


def save_data():
    non_self_gas_df = pd.read_csv('./dummy/non_self_gas_df.csv', encoding='cp949', sep=',')
    self_gas_df = pd.read_csv('./dummy/self_gas_df.csv', encoding='cp949', sep=',')
    non_self_die_df = pd.read_csv('./dummy/non_self_die_df.csv', encoding='cp949', sep=',')
    self_die_df = pd.read_csv('./dummy/self_die_df.csv', encoding='cp949', sep=',')
    return non_self_die_df, non_self_gas_df, self_die_df, self_gas_df


def pre_process(df):
    df['날짜'] = pd.to_datetime(df['날짜'])


class StatPageUI(QMainWindow, stat_UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(fig)
        self.vbox = self.findChild(QVBoxLayout, 'Graph')
        self.setup_custom_ui()

        # CrawlOpiNet()  # 크롤링: 바로 가져오지 않고 크롤링 후 저장한 것을 가져오는 것만으로 괜찮을까? 스레드 사용?

        dataset = None
        # 임시 데이터: UI 초기화 시 데이터를 가져온다?
        while not dataset or len(dataset[0][0]) == 0:
            try:
                non_self_die_df, non_self_gas_df, self_die_df, self_gas_df = save_data() # 저장하고 쓸 데이터 가져옴
                dataset = [[self_gas_df, non_self_gas_df], [self_die_df, non_self_die_df]]  # 같은 속성들을 지닌 df들.
            except Exception as e:
                print(e)
                print(traceback.format_exc())

        for i in 0, 1:
            for j in 0, 1:
                pre_process(dataset[i][j])

        self.cities = dataset[0][0].columns.tolist()[2:]
        self.term = dataset[0][0]['날짜']
        self.pushButton.clicked.connect(lambda: self.plot_data(dataset, fig))
        for i in range(1, len(self.cities) + 1):
            getattr(self, f'checkBox_{i}').stateChanged.connect(lambda: self.plot_data(dataset, fig))

    def setup_custom_ui(self):
        self.vbox.addWidget(self.canvas)
        self.addToolBar(NavigationToolbar(self.canvas, self))
        self.setWindowTitle('최근 일주일 지역별 유가')
        self.unselect_all.clicked.connect(lambda: self.nullify_all_draw())

    def nullify_all_draw(self):
        for i in range(1, len(self.cities) + 1):
            temp = getattr(self, f'checkBox_{i}')
            if temp.isChecked():
                temp.toggle()

    def plot_data(self, dataset, fig):
        # 셀프/비셀프 비교 선택 시 data 전달을 분기
        if self.self_combo.currentIndex() == 0:  # self_combo의 첫 선택지는 셀프/비셀프를 비교한다: dataframe 2개.
            self.plot_data_multi(dataset, fig)
        else:  # 아닌 경우 data frame은 하나.
            self.plot_data_single(dataset, fig)
        try:
            self.explanation.setText(
                '대상 기간: ' + self.term[0].strftime('%Y년 %m월 %d일') + ' ~ ' +  # 출력문은 전달해주는 날짜로 한다: 원하는 날 선택할 수 있도록
                self.term[len(self.term) - 1].strftime('%Y년  %m월 %d일'))
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def plot_data_multi(self, dataset, fig):  # 셀프/비셀프 비교로 그리기
        self.check_ax(fig)

        data = dataset[self.oil_combo.currentIndex()]  # dataframe 2개, self와 비 self

        for j in range(0, 2):
            for i, col in enumerate(data[j].columns[2:], start=1):
                if j == 0:  # self
                    a = '-'
                    labels = [col.split()[0] + '(셀프)' for col in data[j].columns[2:]]
                elif j == 1:  # non-self
                    a = ':'
                    labels = [col.split()[0] + '(비셀프)' for col in data[j].columns[2:]]
                if getattr(self, f'checkBox_{i}').isChecked():
                    self.ax.plot(data[j]['날짜'], data[j][col], label=labels[i - 1], linestyle=a)  # self 인것은 점선, 아닌 것은 실선
        
        self.date_formatter(fig)  # x축 날짜 포멧
        draw_axis(data[0])  # 축 그리기
        self.draw_legend()  # 범례 그리기
        self.canvas.draw()  # 그리기

    def draw_legend(self):
        handles, _ = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend()

    def plot_data_single(self, dataset, fig):  # 하나만 그리기
        self.check_ax(fig)

        if self.self_combo.currentIndex() == 1:  # 셀프
            a = '-'
        elif self.self_combo.currentIndex() == 2:  # 비셀프
            a = ':'

        data = dataset[self.oil_combo.currentIndex()][self.self_combo.currentIndex() - 1]
        # 그래프 그리기
        labels = [col.split()[0] for col in data.columns[2:]]
        for i, col in enumerate(data.columns[2:], start=1):
            if getattr(self, f'checkBox_{i}').isChecked():
                self.ax.plot(data['날짜'], data[col], label=labels[i - 1], linestyle=a)  # self 인것은 점선, 아닌 것은 실선
        
        self.date_formatter(fig)  # x축 날짜 포멧
        draw_axis(data)  # 축 그리기
        self.draw_legend()  # 범례 그리기
        self.canvas.draw()  # 그리기

    def date_formatter(self, fig):
        date_format = mdates.DateFormatter('%m/%d')
        self.ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

    def check_ax(self, fig):
        # ax를 함수 외부에서 초기화된 경우 넘어간다. # 파이썬에 이런 기능이...
        if not hasattr(self, 'ax'):
            self.ax = fig.add_subplot(111)
        self.ax.clear()


class CrawlOpiNet:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

        # 크롤링
        self.initiate_chrome_driver()
        self.find_info()
        self.diesel_df, self.gasoline_df = self.make_datas()
        self.driver.quit()  # close는 활성화된 창만 닫아 크롬이 백그라운드에서 계속 실행된다.

        # 날짜 속성의 데이터를 pandas가 날짜로 다루도록, string으로 받은 숫자 데이터들도 숫자로 형변환한다.
        mod_date_num(self.diesel_df)
        mod_date_num(self.gasoline_df)

        non_self_gas_df = select_attr(self.gasoline_df, '구분', '비셀프')
        self_gas_df = select_attr(self.gasoline_df, '구분', '셀프')
        non_self_die_df = select_attr(self.diesel_df, '구분', '비셀프')
        self_die_df = select_attr(self.diesel_df, '구분', '셀프')

        # 크롤링 안하고 다루기 위해 만든 더미 파일, 날짜는 2024-04-30와 같이 저장되어서 이 파일로 실행하면 x축은 무효한 값이 출력됨
        non_self_gas_df.to_csv('./dummy/non_self_gas_df.csv', encoding='cp949', sep=',')
        self_gas_df.to_csv('./dummy/self_gas_df.csv', encoding='cp949', sep=',')
        non_self_die_df.to_csv('./dummy/non_self_die_df.csv', encoding='cp949', sep=',')
        self_die_df.to_csv('./dummy/self_die_df.csv', encoding='cp949', sep=',')

    def find_info(self):
        try:
            # 페이지 조작
            # 날짜 선택
            self.day_select()
            # 제품 선택
            self.oil_type_select('휘발유')
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        time.sleep(1)
        # 조회
        while not self.click_search():
            print('clicking')
        time.sleep(3)

        return self.make_gasoline_diesel_data()

    def initiate_chrome_driver(self):
        self.driver.get('https://www.opinet.co.kr/user/doposfr/dopOsFrSelect.do')
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="search_form"]/div[2]/ul/li[4]/a').click()
        time.sleep(1)

    def make_gasoline_diesel_data(self):
        # 데이터 가져오기
        datas = self.driver.find_elements('xpath',
                                          '/html/body/div/div[2]/div[2]/div[2]/form/div[6]/div/div/table/tbody/tr')
        data = make_2d_table(datas)
        self.oil_type_select('경유')
        time.sleep(1)
        while not self.click_search():
            print('clicking')
        time.sleep(3)
        datas2 = self.driver.find_elements('xpath',
                                           '/html/body/div/div[2]/div[2]/div[2]/form/div[6]/div/div/table/tbody/tr')
        data2 = make_2d_table(datas2)

        return data, data2

    def click_search(self):
        try:
            self.driver.find_element(By.ID, 'btn_search').click()
            return True
        except selenium.common.exceptions.ElementClickInterceptedException:
            return False

    def oil_type_select(self, oil):
        if oil == '휘발유':
            self.driver.find_element(By.ID, 'rd_pd_2').click()
            time.sleep(1)
        else:
            self.driver.find_element(By.ID, 'rd_pd_3').click()
            time.sleep(1)

    def day_select(self):
        time.sleep(1)
        Select(self.driver.find_element(By.ID, 'STA_D'))
        seven_days_ago = get_previous_date(7)
        month = seven_days_ago.month
        day = seven_days_ago.day
        # 일주일 치 선택
        Select(self.driver.find_element(By.ID, 'STA_D')).select_by_index(day - 1)
        time.sleep(1)
        Select(self.driver.find_element(By.ID, 'STA_M')).select_by_index(month - 1)
        time.sleep(1)

    def make_datas(self):
        gasoline_info, diesel_info = self.find_info()
        table_header = ['날짜']
        self.make_header(table_header)
        gasoline_df = pd.DataFrame(gasoline_info, columns=table_header)
        diesel_df = pd.DataFrame(diesel_info, columns=table_header)
        return diesel_df, gasoline_df

    def make_header(self, table_header):
        header_rows = self.driver.find_elements(By.XPATH,
                                                '/html/body/div/div[2]/div[2]/div[2]/form/div[6]/div/div/table/thead/tr')
        for row in header_rows:
            th_elements = row.find_elements(By.TAG_NAME, 'th')
            row_data = [th.text for th in th_elements]
            table_header.extend(row_data)
