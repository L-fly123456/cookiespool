import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
from weibo.chaojiying import Chaojiying_Client

CHAOJIYING_USERNAME='18192416361'
CHAOJIYING_PASSWORD='a1335108246'
CHAOJIYING_SOFT_ID=902020
CHAOJIYING_KIND=9004

EMAIL = "18192416361"
PASSWORD = "a1335108246"
BORDER = 6

class Crack():
    def __init__(self):
        self.url = "https://passport.weibo.cn/signin/login"
        self.email = EMAIL
        self.password = PASSWORD
        self.browser = webdriver.Chrome()
        # self.get=self
        self.wait = WebDriverWait(self.browser, 15)
        self.chaojiying=Chaojiying_Client(CHAOJIYING_USERNAME,CHAOJIYING_PASSWORD,CHAOJIYING_SOFT_ID)
    def open(self):
        email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#loginName")))
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#loginPassword")))
        email.send_keys(self.email)
        time.sleep(2)
        password.send_keys(self.password)
        time.sleep(2)
    def login(self):
        submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn")))
        submit.click()
        # time.sleep(1)
        # print("登陆成功！")
    def get_geetest_button(self):
        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.geetest_radar_tip")))
        button.click()
    def go(self):
        self.browser.get(self.url)
        self.browser.maximize_window()
        self.open()
        time.sleep(1)
        self.login()
        button = self.get_geetest_button
        button()
        # time.sleep(15)

if __name__=="__main__":
    Crack().go()




