from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
import time
from requests import Session
from weibo.chaojiying import Chaojiying_Client
from selenium.common.exceptions import TimeoutException
from weibo.crack import Crack

EMAIL='18192416361'
PASSWORD='a1335108246'
# 超级鹰用户名，密码，软件id,验证码类型
CHAOJIYING_USERNAME='18192416361'
CHAOJIYING_PASSWORD='a1335108246'
CHAOJIYING_SOFT_ID=902020
CHAOJIYING_KIND=9004
class weibo_click():
    def __init__(self,username,password,browser):
        # self.url = "https://passport.weibo.cn/signin/login"
        self.email = username
        self.password = password
        self.browser=browser
        # self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 15)
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
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
        # self.browser.get(self.url)
        self.browser.maximize_window()
        self.open()
        time.sleep(1)
        self.login()
        # self.get_geetest_button()

    def get_screenshot(self):  # 截图功能
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot
    def get_position(self):
        '''
        获取点触验证码位置
        :return: 点触验证码位置元组
        '''
        img=self.get_weibo_element()
        # img =self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_item_img ")))
        time.sleep(1)
        location = img.location
        size = img.size
        print(location)
        print(size)
        top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], \
                                   location["x"] + size["width"]
        return (top, bottom, left, right)
    def click_image(self):
        '''
        点触验证码截图
        :return: 点触验证码对象
        '''
        top, bottom, left, right = self.get_position()
        print("验证码位置", top, bottom, left, right)
        screenshot = self.get_screenshot()
        # screenshot.show()
        print('大图尺寸,', screenshot.size)
        captcha = screenshot.crop((833, 200, 1252, 632))  # crop方法是Image里的截图方法 先后顺序有规定（左，上，右，下）
        captcha.save('bbb.png')
        # captcha.show()
        print('小图尺寸,', captcha.size)
        # img = Image.open(name)
        (x, y) = captcha.size
        x_s = 334
        y_s = round(y * x_s / x)
        out_img = captcha.resize((x_s, y_s), Image.ANTIALIAS)
        out_img.save('ccc.png')
        # out_img.show()
        return out_img
    def result(self):
        image = self.click_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 识别验证码
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        return result
    def get_points(self, captcha_result):
        '''
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        '''
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        print(locations)
        return locations
    def get_weibo_element(self):
        '''
        获取点触验证码对象
        :return: 图片对象
        '''
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_item_img ")))
        return element
    def weibo_click_words(self,locations):
        '''
        点击验证码图片
        :param locations: 点击位置
        :return: None
        '''
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_weibo_element(),location[0],location[1]).click().perform()
            time.sleep(1)

    def confirm(self):
        push=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.geetest_commit_tip")))
        push.click()
    def main(self):
        print('点触验证码的验证')
        while True:
            captcha_result = self.result()
            locations = self.get_points(captcha_result)
            self.weibo_click_words(locations)
            button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.geetest_commit_tip")))
            button.click()
            if self.login_successfully():
                break
            else:
                continue


    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误'))
        except TimeoutException:
            return False

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.m-text-cut"))))
        except TimeoutException:
            return False

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()

    def man(self):
        """
        破解入口
        :return:
        """
        self.go()
        # 验证账号和密码
        if self.password_error():
            email = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#loginName")))
            password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#loginPassword")))
            email.clear()
            password.clear()
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }

        # 不需要验证直接登录
        if self.login_successfully():
            cookies = self.get_cookies()
            print('cookies',cookies)
            return {
                'status': 1,
                'content': cookies
            }
        # 账号密码没错并需要验证就获取图片对象
        self.get_geetest_button()
        self.main()
        # 判断是否登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            print('cookies',cookies)
            return {
                'status': 1,
                'content': cookies
            }
        else:
            return {
                'status': 3,
                'content': '登录失败'
            }

if __name__=="__main__":
    weibo_click('fub1567437@163.com', 'wpmtnbs68v').man()