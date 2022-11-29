import requests as req
import allure
import pytest
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

@pytest.mark.fb_link_verify
@allure.story("驗證下拉式選單中Facebook連結是否正確")
def test_fb_link():
    driver = openBrowser()
    req_text = req_data_fb(driver)
    sel_text = sel_data_fb(driver)
    assert req_text == sel_text
    closeBrowser(driver)

@pytest.mark.ins_link_verify
@allure.story("驗證下拉式選單中的Instagram連結是否正確")
def test_ins_link():
    driver = openBrowser()
    req_title = req_data_ins(driver)
    sel_title = sel_data_ins(driver)
    print(req_title,sel_title)
    assert req_title == sel_title
    closeBrowser(driver)

@pytest.mark.menu_test
@allure.story("下拉式選單下排文字驗證")
def test_scroll_menu():
    driver = openBrowser()
    game_text = game_menu(driver)
    hardware_text = hardware_menu(driver)
    game_answer = "PS5,PS4,PS VR,PS Plus,購買遊戲"
    hardware_answer = "PS5,PS4,PS4 Pro,PS VR2"
    assert game_text == game_answer, hardware_text == hardware_answer
    closeBrowser(driver)

@allure.step("開啟瀏覽器")
def openBrowser():
    s = Service(r"./chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    return driver

@allure.step("關閉瀏覽器")
def closeBrowser(driver):
    driver.quit()

@allure.step("使用requests拿後端資料(Facebook)")
def req_data_fb(driver):
    url = "https://social.playstation.com/jetstream/quicklinks/zh-hant-tw.json"
    headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = req.get(url, headers=headers)
    all = json.loads(r.text)
    target = all['msg_news'][0]['link']
    driver.get(target)
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div[1]/span/h1"))
    )
    req_text = content.text
    return req_text
    
@allure.step("使用selenium拿取前端資料(Facebook)")
def sel_data_fb(driver):
    driver.get("https://zh-tw.facebook.com/PlayStationTaiwan")
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div[1]/span/h1"))
    )
    sel_text = content.text
    return sel_text 
    
@allure.step("使用requests後端資料(Instagram)")
def req_data_ins(driver):
    url = "https://social.playstation.com/jetstream/quicklinks/zh-hant-tw.json"
    headers ={
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = req.get(url, headers=headers)
    all = json.loads(r.text)
    target = all["msg_news"][1]["link"]
    driver.get(target)
    text_tmp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/div[1]/h2"))
    )
    req_title = text_tmp.text
    return req_title

@allure.step("使用selenium取得前端資料(Instagram)")
def sel_data_ins(driver):
    driver.get("https://www.instagram.com/playstationtaiwan/?hl=en&smcid=pdc%3Azh-hant-tw%3Aprimary%20nav%3Amsg-news%3Ainstagram")
    text_tmp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/div[1]/h2"))
    )
    sel_title = text_tmp.text
    return sel_title

@allure.step("下拉式選單_遊戲")
def game_menu(driver):
    driver.get("https://www.playstation.com/zh-hant-tw/")
    time.sleep(5)
    game_button = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[1]/button"))
        )
    game_button.click()
    time.sleep(5)
    ps5_temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[1]/div/div/section/div[1]/a/span"))
    )
    ps5_text = ps5_temp.text
    ps4_temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[1]/div/div/section/div[2]/a/span"))
    )
    ps4_text = ps4_temp.text
    vr_temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[1]/div/div/section/div[3]/a/span"))
    )
    vr_text = vr_temp.text
    plus_temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[1]/div/div/section/div[4]/a/span"))
    )
    plus_text = plus_temp.text
    buy_temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[1]/div/div/section/div[5]/a/span"))
    )
    buy_text = buy_temp.text
    game_all_text = ps5_text + "," + ps4_text + "," + vr_text + "," + plus_text + "," + buy_text
    return game_all_text

@allure.step("下拉式選單_硬體")
def hardware_menu(driver):
    driver.get("https://www.playstation.com/zh-hant-tw/")
    driver.refresh()
    time.sleep(5)
    hardware_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[2]/button"))
    )
    hardware_button.click()
    time.sleep(5)
    ps5_temp2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[2]/div/div/section/div[1]/a/span"))
    )
    ps5_text2 = ps5_temp2.text
    ps4_temp2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[2]/div/div/section/div[2]/a/span"))
    )
    ps4_text2 = ps4_temp2.text
    pro4_temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[2]/div/div/section/div[3]/a/span"))
    )
    pro4_text = pro4_temp.text
    vr2_temp = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/section/div/header/nav/div/section/div[2]/div/div/section/div[4]/a/span"))
    )
    vr2_text = vr2_temp.text
    hardware_all_text = ps5_text2 + "," + ps4_text2 + "," + pro4_text + "," + vr2_text
    return hardware_all_text