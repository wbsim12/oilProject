import os, sys, traceback, requests, time, json
import pandas as pd
# pyQt 라이브러리 임포트
from PyQt5.QtCore import QUrl
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# driver = webdriver.Chrome()
#
# options = webdriver.ChromeOptions()
# options.add_argument('--headless') # 창이 나타나지 않도록 headless
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(options=options)
class kakao_map_set():
    def set_url(self):
        return "http://localhost:8000/kao_index.html"


    def oil_price_search(self):
        try:
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=options)
            url = "https://www.opinet.co.kr/searRgSelect.do"
            driver.get(url)

            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#SIDO_NM0"))
            )
            element.send_keys("경기")

            element1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#SIGUNGU_NM0"))
            )
            element1.send_keys("성남시")

            element2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(('xpath', '//*[@id="templ_list0"]/div[7]/div/a'))
            )
            element2.click()
            time.sleep(2)

            # driver.implicitly_wait(7)
            # driver.find_element("css selector", "#SIDO_NM0").send_keys("경기")
            # driver.implicitly_wait(7)
            # driver.find_element("css selector", "#SIGUNGU_NM0").send_keys("성남시")
            #
            # driver.implicitly_wait(10)
            # driver.find_element("xpath", '//*[@id="templ_list0"]/div[7]/div/a').click()
            # time.sleep(2)

        except Exception as e:
            print(e)
            print(traceback.format_exc())

    def read_xls_to_csv(self):
        excels = 'C:/Users/USER/Downloads/지역_위치별(주유소).xls'
        df = pd.read_excel(excels, header=2)
        print(df)
        df.to_csv('./dummy/oil_price.csv', encoding='utf-8', index=False)

    def read_csv_rename_df(self):
        df_csv = pd.read_csv('./dummy/oil_price.csv', encoding='utf-8')
        #print(df_csv)
        new_df = df_csv[['상호', '주소', '휘발유', '경유']]
        new_column_names = {
            '상호' : 'name',
            '주소' : 'address',
            '휘발유' : 'gasoline',
            '경유' : 'diesel'
        }
        rename_df = new_df.rename(columns=new_column_names)

        #print(new_df, type(new_df))
        rename_df.to_csv('./dummy/oil_price_new.csv', encoding='utf-8', index=False)

    def read_csv_add_xy(self):
        df = pd.read_csv('./dummy/oil_price_new.csv', encoding='utf-8')
        address = df.loc[:, ['address']]
        #print(address, type(address))
        lati = []
        longti = []

        for i, row in address.iterrows():
            try:
                # print(i)
                #print(row['주소'])
                a = kakao_map_set.get_location(self, row['address'])
                #print(a)
                a2 = list(a.values())

                lati.append(a2[0])
                #print(a2[0])
                longti.append(a2[1])
                #print(a2[1])
                #print(a, "코딩 성공")
            except AttributeError as e:
                print(i, "코딩 실패")
                print(e)
        #
        # print(lati)
        # print(longti)
        #
        #
        df['x'] = longti
        df['y'] = lati
        df.to_csv('./dummy/oil_price_to_json.csv', encoding='utf-8', index=False)
        df.to_csv('./result_file/oil_price.csv', encoding='cp949', index=False)

    def read_csv_to_json(self):
        df = pd.read_csv('./dummy/oil_price_to_json.csv')
        json_list = []
        for i, row in df.iterrows():
            json_obj = {
                'name': row['name'],
                'address': row['address'],
                'gasoline': row['gasoline'],
                'diesel': row['diesel'],
                'x': row['x'],
                'y': row['y']
            }
            json_list.append(json_obj)

        with open('./html/output.json', 'w') as json_file:
            json.dump(json_list, json_file, indent=4)


    def get_location(self, address):

        url = "https://dapi.kakao.com/v2/local/search/address.json"
        api_key = "7573339f0fecfa2f4e8c33364dce0d73"

        headers = {
            "Authorization": f"KakaoAK {api_key}"
        }
        params = {
            "query": address
        }
        response = requests.get(url, headers=headers, params=params)
        result = response.json()

        if result["meta"]["total_count"] > 0:
            # 결과가 있는 경우 첫 번째 결과의 좌표 반환
            coords = {
                "x": result["documents"][0]["x"],
                "y": result["documents"][0]["y"]
            }
            return coords
        else:
            # 결과가 없는 경우 None 반환
            return None
