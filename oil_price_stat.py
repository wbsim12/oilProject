import os, sys
import pandas as pd
import numpy as np
import traceback

from PyQt5 import uic
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('Qt5Agg')


oil_df = pd.read_csv('./data/avg_selling-price.csv', encoding='cp949', sep=',')

root = os.path.dirname(os.path.abspath(__file__))
stat_UI = uic.loadUiType(os.path.join(root, 'oil_stat.ui'))[0]


def select_attr(df, attr, val):  # 해당 속성의 값들만 골라내고 그 속성은 drop한다.
    return df[df[attr] == val].drop(attr, axis=1)


def mod_date(df):
    df['기간'] = pd.to_datetime(df['기간'], format='%Y%m%d')


class OilStatPage(QMainWindow, stat_UI):
    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('연간 유형별 지역 유가')

            mod_date(oil_df)

            self_pat_df = select_attr(oil_df, '구분', '셀프')
            non_self_pat_df = select_attr(oil_df, '구분', '비셀프')
            self_disel_df = select_attr(oil_df, '구분', '셀프')
            non_self_diesl_df = select_attr(oil_df, '구분', '셀프')

            df_list = [[self_pat_df, non_self_pat_df], [self_disel_df, non_self_diesl_df]]


            vbox = self.findChild(QVBoxLayout, 'Graph1')
            self.draw(vbox, self_pat_df)

            vbox.addWidget(self.canvas)
            vbox.deleteWidget()
            self.addToolBar(NavigationToolbar(self.canvas, self))


            self.patrolium.isChecked().connect(lambda: self.draw())

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def draw(self, vbox, df):
        # 지우고
        while vbox.count():
            child = vbox.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 만든다
        self.canvas = MplCanvas(df)

        vbox.addWidget(self.canvas)
        self.canvas.draw()


class MplCanvas(FigureCanvas):
    def __init__(self, df, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

        labels = [col.split()[0] for col in df.columns[1:]]

        print(labels)

        for i, col in enumerate(df.columns[1:], start=1):  #
            self.axes.plot(df['기간'], df[col], label=labels[i-1])

        self.axes.set_xlabel('Date')
        self.axes.set_ylabel('Oil Price')

        date_format = mdates.DateFormatter('%m/%d')
        self.axes.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()

        self.axes.legend()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    statPage = OilStatPage()
    statPage.show()
    sys.exit(app.exec_())
