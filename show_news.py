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

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QPushButton, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

root = os.path.dirname(os.path.abspath(__file__))
# ui만든 파일의 경로
MainUI = uic.loadUiType(os.path.join(root, 'main.ui'))[0]
driver = webdriver.Chrome()

class MainDialog(QMainWindow, MainUI):
    def __init__(self):
        try:
            super().__init__()
            self.cnt = 0
            self.setupUi(self)
            self.set_driver()
            self.get_latest_news()
            self.relv_btn.clicked.connect(self.get_relevance_news)
            self.latest_btn.clicked.connect(self.get_latest_news)
            self.scrab_btn.clicked.connect(self.scrap_news)

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def set_driver(self):
        try:
            url = "https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EC%9C%A0%EA%B0%80"  # url 설정
            driver.get(url)
            print("페이지 타이틀:", driver.title)
        except Exception as e:
            print("오류 발생:", e)

    def get_latest_news(self):  # 최신순 뉴스'
        title = ''
        driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[1]/a[2]').click()
        news_titles_new = driver.find_elements(By.CLASS_NAME, "news_tit")
        for news_title_new in news_titles_new:
            # title = title + news_title_new.text + '\n'
            link = news_title_new.get_attribute('href')
            text = news_title_new.text
            if '유가증권' not in text:
                title += f"<a href='{link}'>{text}</a><br>"

        self.show_news_label.setText(title)
        self.get_news_page(self.show_news_label)



    def get_relevance_news(self): #관련도순 뉴스'
        try:
            title=''
            driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[1]/a[1]').click()
            news_titles_relv = driver.find_elements(By.CLASS_NAME, "news_tit")
        #   news_titles_relv_smry = driver.find_elements(By.CLASS_NAME, "api_txt_lines dsc_txt_wrap")

            for news_title_relv in news_titles_relv:
                #title = title + news_title_new.text + '\n'
               # title += f"<a href='{news_title_relv.get_attribute('href')}'>{news_title_relv.text}</a><br>"
                link = news_title_relv.get_attribute('href')
                text = news_title_relv.text
                if '유가증권' not in text:
                    title += f"<a href='{link}'>{text}</a><br>"
              #  self.scrap.append({'Title': text, 'Url': link})
            self.show_news_label.setText(title)
            self.get_news_page(self.show_news_label)

        except Exception as e:
            print(e)
            print(traceback.format_exc())
   # def do_scrap(self, scr_box):
       # df = pd.DataFrame(scr_box, columns=['Title'])
        #df.to_csv('./scrap.csv', mode='a', header=True, index=False)

    def get_news_page(self, label):
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 텍스트를 브라우저처럼 상호 작용 가능하도록 설정합니다.
        label.setOpenExternalLinks(True)  # 외부 링크를 클릭했을 때 브라우저에서 열도록 설정합니다.
        #label.setText(text)  # HTML 형식의 텍스트를 설정합니다.

    def scrap_news(self):
        try:
            scr_box = []
            scr_text = self.show_news_label.text()
            for news_title in scr_text.split('<br>'):
                scr_box.append({'Title': news_title})
                print(news_title)
            # self.do_scrap(scr_box)
        except Exception as e:
            print(e)
            print(traceback.format_exc())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())




