import os, sys
import pandas as pd
import traceback
import time
from datetime import datetime, timedelta

import selenium.common.exceptions
from PyQt5 import uic
from PyQt5.QtWidgets import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
root = os.path.dirname(os.path.abspath(__file__))
stat_UI = uic.loadUiType(os.path.join(root, 'oil_stat.ui'))[0]


def select_attr(df, attr, val):  # 해당 속성의 값들만 골라내고 그 속성은 drop한다.
    return df[df[attr] == val].drop(attr, axis=1)


def mod_date_num(df):
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')
    city_names = list(df.columns[2:])
    for city in city_names:
        df[city] = df[city].str.replace(',', '').astype(float)


def get_previous_date(days):
    previous_date = datetime.today() - timedelta(days=days)
    return previous_date.month, previous_date.day


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
    temp_sum = 0

    city_list = df[0, 2:]
    for city in city_list:
        max_temp = df[city].max()
        min_temp = df[city].min()
        temp_sum += df[city].sum()
        if ret_max < max_temp:
            ret_max = max_temp
        if ret_min > min_temp:
            ret_min = min_temp
    return ret_max, ret_min, temp_sum / (len(city_list) * len(df))


class OilStatPage(QMainWindow, stat_UI):
    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            self.initiate_chrome_driver()

            fig = Figure(figsize=(5, 4), dpi=100)
            self.canvas = FigureCanvas(fig)
            self.vbox = self.findChild(QVBoxLayout, 'Graph')
            self.vbox.addWidget(self.canvas)
            self.addToolBar(NavigationToolbar(self.canvas, self))
            self.setWindowTitle('최근 일주일 지역별 유가')

            # 크롤링
            self.find_info()  # 스레드 적용 해야 함.
            self.diesel_df, self.gasoline_df = self.make_datas()
            self.driver.close()

            mod_date_num(self.diesel_df)
            mod_date_num(self.gasoline_df)

            non_self_gas_df = select_attr(self.gasoline_df, '구분', '비셀프')
            self_gas_df = select_attr(self.gasoline_df, '구분', '셀프')
            non_self_die_df = select_attr(self.diesel_df, '구분', '비셀프')
            self_die_df = select_attr(self.diesel_df, '구분', '셀프')

            dataset = [[self_gas_df, non_self_gas_df], [self_die_df, non_self_die_df]]

            self.pushButton.clicked.connect(lambda: self.plot_data(dataset, fig))

        except Exception as e:
            print(e)
            print(traceback.format_exc())

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

    def initiate_chrome_driver(self):
        self.driver.get('https://www.opinet.co.kr/user/doposfr/dopOsFrSelect.do')
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="search_form"]/div[2]/ul/li[4]/a').click()
        time.sleep(1)

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
        month, day = get_previous_date(7)
        # 일주일 치 선택
        Select(self.driver.find_element(By.ID, 'STA_D')).select_by_index(day - 1)
        time.sleep(1)
        Select(self.driver.find_element(By.ID, 'STA_M')).select_by_index(month - 1)
        time.sleep(1)

    def plot_data(self, dataset, fig):  # 살펴볼 것
        data = dataset[self.oil_combo.currentIndex()][self.self_combo.currentIndex()]
        # 그래프 그리기
        ax = fig.add_subplot(111)
        labels = [col.split()[0] for col in data.columns[2:]]

        for i, col in enumerate(data.columns[2:], start=1):
            ax.plot(data['날짜'], data[col], label=labels[i - 1])

        date_format = mdates.DateFormatter('%m/%d')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

        try:
            max, min, avg = find_max_min_avg(data)
            plt.ylim(min - 50, max + 50)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        ax.legend()
        self.canvas.draw()
        print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    statPage = OilStatPage()
    statPage.show()
    sys.exit(app.exec_())
