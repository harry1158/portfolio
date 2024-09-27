from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
import csv

chrome_options = webdriver.ChromeOptions()

@dataclass
class House:
    Name: str = ""
    traffic: str = ""
    money: str = ""
    link: str = ""
    net: str = ""
    shere: str = ""
    parking: str = ""

def main(page, cnt):
    driver = webdriver.Chrome(options=chrome_options)
    URL = f"https://sumaity.com/chintai/theme/single/{"場所してい"}?page={page}"
    driver.get(URL)
    
    building_elements = driver.find_elements(By.CLASS_NAME, "building")
    # すべてのdata-idを格納するリスト
    id_list = []
    # 各div要素のdata-id属性を取得
    for element in building_elements:
        data_id = element.get_attribute("data-id")
        if data_id:  # data-idが存在する場合
            id_list.append(data_id)

    # houseデータを保存するリスト
    data = []
    for i in range(cnt):
        # ループごとに新しい House インスタンスを作成
        house_instance = House()
        
        # test 関数で house インスタンスにデータを格納
        test(driver, id_list[i], house_instance)
        
        # house インスタンスをリストに追加
        data.append(house_instance)
        print(f"page: {page},cunt {i+1}")

    # ドライバを閉じる
    driver.quit()
    write_to_csv(data)

def test(driver, data_id, house_instance):
    try:
        # 指定された data-id を持つ建物を取得
        building = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@data-id='{data_id}']"))
        )
        house_instance.Name = building.find_element(By.CSS_SELECTOR, "div.buildingName a").text
        house_element = building.find_element(By.CSS_SELECTOR, "div.buildingName a")
        house_instance.link = house_element.get_attribute("href")
        
        ul_traffic = WebDriverWait(building, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "traffic"))
        )
        li_elements = ul_traffic.find_elements(By.TAG_NAME, "li")
        traffic_text = ""
        for li in li_elements:
            line_text = li.text
            traffic_text += f'{line_text}\n'
        house_instance.traffic = traffic_text
        # detail 関数で詳細情報を取得
        detail(driver, house_instance.link, house_instance)
    except:
        print(data_id)
        house_instance.link = f"https://sumaity.com/chintai/tokyo_bldg/bldg_{data_id}/"
        

def detail(driver, URL, house_instance):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)
    money = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "p-building-summary-basic__price"))
    )
    house_instance.money = money.text
    
    categories = ["インターネット・TV", "共用部", "駐車場・駐輪場"]
    arr = []
    for category in categories:
        try:
            th_element = driver.find_element(By.XPATH, f'//th[text()="{category}"]')
            td_element = th_element.find_element(By.XPATH, 'following-sibling::td')
            td_value = td_element.text
            arr.append(td_value)
        except NoSuchElementException:
            arr.append("")

    house_instance.net = arr[0]
    house_instance.shere = arr[1]
    house_instance.parking = arr[2]
    driver.quit()
    
def write_to_csv(data):
    # CSVファイルに書き込む (UTF-8 with BOM でエンコード)
    with open('houses_data.csv', mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        # ヘッダーを書き込み
        writer.writerow(["Name", "Traffic", "Money", "Link", "Net", "Shere", "Parking"])
        
        # データを書き込み
        for house in data:
            writer.writerow([house.Name, house.traffic, house.money, house.link, house.net, house.shere, house.parking])

# 実行
for i in range(30):
    main(i+1+16, 30)
    print (f"page{i+1}終了")
