import os, sys
import traceback

import sys
# pyQt 라이브러리 임포트
from PyQt5.QtCore import QUrl
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
root = os.path.dirname(os.path.abspath(__file__))
# ui만든 파일의 경로
MainUI = uic.loadUiType(os.path.join(root, 'testMain.ui'))[0]

class MainDialog(QMainWindow, MainUI):


    # init은 맨 처음 수행되고 동작안함(초기화)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("다이나믹 맵 테스트")
        self.web_view.load(QUrl("http://localhost:8000/kao_index.html"))
        # with open('http://localhost:8000/', 'r', encoding='utf-8') as f:
        #     html_content = f.read()
        # self.web_view.setHtml(html_content)

    # def load_kakao_map(self):
    #     # Kakao Map API를 사용한 HTML 페이지 URL
    #     url = QUrl.fromLocalFile("http://localhost:8080")  # HTML 파일 경로 입력
    #     self.web_view.load(url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainDialog()
    mainWindow.show()
    sys.exit(app.exec_())
