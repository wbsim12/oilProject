from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#pip3 install -U selenium
#최신버전의 셀레니움 사용시 크롬드라이브 다운받을 필요없음
import os, sys
import pandas as pd
from PyQt5 import uic
import traceback
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from get_whole_price import show_prices
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QPushButton, QVBoxLayout, QLabel, \
    QTextEdit, QTabBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer, QUrl
from oil_price_stat import *
from avg_recent_price import avg_price
from kakao_map_test import kakao_map_set

#import kakao_map_test
from oil_price_stat import *

root = os.path.dirname(os.path.abspath(__file__))
# ui만든 파일의 경로
MainUI = uic.loadUiType(os.path.join(root, 'ui/main.ui'))[0]
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 창이 나타나지 않도록 headless
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)


class MainDialog(QMainWindow, MainUI):
    def __init__(self):
        try:
            super().__init__()
            self.cnt = 0
            self.setupUi(self)
            self.set_driver()
            self.apply_stylesheet("html/style.css")  # CSS 파일 적용
          #  self.latest_btn.setStyleSheet('background:#f7f7f7; color: black;')
          #  self.relv_btn.setStyleSheet('background:#f7f7f7; color: black;')
            self.show_news_label.setStyleSheet('font-size: 15px;')
            self.latest_btn.setStyleSheet('border: none;')
            self.relv_btn.setStyleSheet('border: none;')
            self.get_latest_news()
            self.relv_btn.clicked.connect(self.get_relevance_news)
            self.latest_btn.clicked.connect(self.get_latest_news)
            self.scrab_btn.clicked.connect(self.scrap_news)
            self.tabBar = self.tabWidget.findChild(QTabBar)
            self.tabBar.hide()
            all_check1, all_check2, all_check3, all_check4 = show_prices.show_all_prices(self)                            ##박영욱
            local_check1, local_check2, local_check3, local_check4 = show_prices.show_local_prices(self)
            self.label_12.setText("전국평균(원/리터)\n휘발유 {:.2f}원 (전일대비 {:+.2f}원)\n경유 {:.2f}원 (전일대비 {:+.2f}원)".format(all_check1, all_check2,all_check3, all_check4))
            self.label_11.setText("성남평균(원/리터)\n휘발유 {:.2f}원 (전일대비 {:+.2f}원)\n경유 {:.2f}원 (전일대비 {:+.2f}원)".format(local_check1,local_check2,local_check3,local_check4))
            self.scrap_box = []
            self.cheapest_btn.clicked.connect(self.move_page)
            self.oil_price_btn.clicked.connect(self.oil_price_page)
            self.main_cover_btn_1.clicked.connect(self.get_main)
            self.main_cover_btn_2.clicked.connect(self.get_main)
            self.main_cover_btn_3.clicked.connect(self.get_main)

            try:
                self.price_chart = StatPageUI()
                self.graphLayout.addWidget(self.price_chart)
                self.self_btn.clicked.connect(lambda: self.tabWidget.setCurrentIndex(2))
            except Exception as e:
                print(e)
                print(traceback.format_exc())

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def get_main(self):
        try:
            self.tabWidget.setCurrentIndex(0)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def oil_price_page(self):
        try:
            fig = avg_price.plot_graph(self)
            plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
            self.web_price_view.setHtml(plot_html)
            self.tabWidget.setCurrentIndex(3)
        except Exception as e:
            print(e)
            print(traceback.format_exc())


    def move_page(self):
        try:
            km = kakao_map_set

            url = km.set_url(self)
            print(url)
            self.web_view.load(QUrl(url))
            self.tabWidget.setCurrentIndex(1)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        #kakao_map_test().

    def apply_stylesheet(self, file_path): #css파일 적용
        try:
            with open(file_path, "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception as e:
            print("오류 발생:", e)
    def set_driver(self): #드라이버 설정
        try:
            url = "https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%9C%A0%EA%B0%80"  # url 설정
            driver.get(url)
            print("페이지 타이틀:", driver.title)
        except Exception as e:
            print("오류 발생:", e)

    def get_latest_news(self):  # 최신순 뉴스'
        self.scrap_box = [{'Title': None, 'Url': None}]
        self.latest_btn.setStyleSheet('font-weight: bold; background-color : #f7f7f7;color : black; ')
        self.relv_btn.setStyleSheet('font-weight: normal; background-color : #f7f7f7;color : black; ')
        self.scrab_btn.setText('전체 뉴스 스크랩')
        self.scrab_btn.setStyleSheet('background-color:#405E96')
        title = ''
        driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[1]/a[2]').click()
        news_titles_new = driver.find_elements(By.CLASS_NAME, "news_tit")
        news_titles_new = news_titles_new[:8]  # 처음 8개의 뉴스만 선택
        for news_title_new in news_titles_new:
            # title = title + news_title_new.text + '\n'
            link = news_title_new.get_attribute('href')
            text = news_title_new.text
            if '유가증권' not in text:
                title += f"<a href='{link}'>{text}</a><br>"
                self.scrap_box.append({'Title': text, 'Url': link})
        self.show_news_label.setText(title)
        self.get_news_page(self.show_news_label)

    def get_relevance_news(self): #관련도순 뉴스'
        try:
            self.scrap_box = [{'Title': None, 'Url': None}]
            self.relv_btn.setStyleSheet('font-weight: bold; background-color : #f7f7f7;color : black')
            self.latest_btn.setStyleSheet('font-weight: normal; background-color : #f7f7f7;color : black')
            self.scrab_btn.setText('전체 뉴스 스크랩')
            self.scrab_btn.setStyleSheet('background-color:#405E96')
            title=''
            driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[1]/a[1]').click()
            news_titles_relv = driver.find_elements(By.CLASS_NAME, "news_tit")
        #   news_titles_relv_smry = driver.find_elements(By.CLASS_NAME, "api_txt_lines dsc_txt_wrap")
            news_titles_relv = news_titles_relv[:8]  # 처음 8개의 뉴스만 선택
            for news_title_relv in news_titles_relv:
                link = news_title_relv.get_attribute('href')
                text = news_title_relv.text
                if '유가증권' not in text:
                    title += f"<a href='{link}'>{text}</a><br>"
                    self.scrap_box.append({'Title': text, 'Url': link})
            self.show_news_label.setText(title)
            self.get_news_page(self.show_news_label)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
    def get_news_page(self, label): #뉴스페이지 보여주기
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 텍스트를 브라우저처럼 상호 작용 가능하도록 설정합니다.
        label.setOpenExternalLinks(True)  # 외부 링크를 클릭했을 때 브라우저에서 열도록 설정합니다.
        #label.setText(text)  # HTML 형식의 텍스트를 설정합니다.

    def scrap_news(self):
       # self.scrab_btn.setStyleSheet('background-color:#6C757D')
       # self.scrab_btn.setStyleSheet('background-color:#6C757D')
        self.scrab_btn.setStyleSheet("""
        QPushButton {
            background-color: #6C757D; 
            border: 1px solid #6C757D;
            color:black;
        }
    """)

        self.scrab_btn.setText('스크랩 완료')
        try:
            df = pd.DataFrame(self.scrap_box, columns=['Title', 'Url'])
            df.to_csv('./scrap.csv', mode='a', header=True, index=False)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())



