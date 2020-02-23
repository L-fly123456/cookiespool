import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from selenium.webdriver import ActionChains
import time
from weibo.crack import Crack

EMAIL = "1819241****"
PASSWORD = "a133510****"
BORDER = 5

class CrackGeetest(Crack):
    def __init__(self):
        Crack.__init__(self)

    def get_geetest_image(self,img,name="captcha.png"):
        time.sleep(2)
        location = img.location
        size = img.size
        print(location)
        print(size)
        top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], \
                                   location["x"] + size["width"]
        print("验证码位置", top, bottom, left, right)
        screenshot = self.get_screenshot()
        screenshot.show()
        print('大图尺寸,',screenshot.size)
        captcha = screenshot.crop((833, 205, 1192, 660))  # crop方法是Image里的截图方法 先后顺序有规定（左，上，右，下）
        captcha.save(name)
        (x, y) = captcha.size
        x_s = 260
        y_s = round(y * x_s / x)
        out_img = captcha.resize((x_s, y_s), Image.ANTIALIAS)
        out_img.save(name)
        out_img.show()
        return out_img

    def get_screenshot(self):  # 截图功能
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_slider_button")))
        return slider

    def is_pixel_equal(self, image1, image2, x, y):
        pixel1 = image1.load()[x, y]  # 带缺口图片
        pixel2 = image2.load()[x, y]  # 不带缺口图片
        print('pixel1:',pixel1)
        print('pixel2',pixel2)
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        left = 80
        print('image1.size[0]',image1.size[0])
        print('image1.size[1]',image1.size[1])
        for i in range(left, image1.size[0]):  # 从x轴的60开始遍历
            for j in range(image1.size[1]):  # y轴
                print(i,j)
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    print("left",left)
                    return left
        return left

    def get_track(self, distance):
        current = 0  # 当前距离
        mid = distance * 4 / 5  # 到mid时减速
        V = 0  # 初速度为0
        track = []  # 移动轨迹
        t = 0.2  # 时间
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            V0 = V  # 初速度为0赋值给V0，下一循环后的初速度是上一循环时的速度
            V = V0 + a * t  # 得到加速度后的速度
            move = V0 * t + a * t * t / 2  # 移动距离
            current += move  # 移动后的距离
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack(self):
        self.go()
        print('滑块验证码的验证')
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_canvas_slice ")))
        image1 = self.get_geetest_image(img, "captcha1.png")
        self.browser.execute_script('document.querySelectorAll("canvas")[2].style=""')
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_canvas_slice ")))
        image2 = self.get_geetest_image(img, "captcha2.png")
        gap = self.get_gap(image1, image2)
        print("缺口位置", gap)
        gap = gap - BORDER  # 拼图左边和图片边缘有6的距离 所以减去6
        track = self.get_track(gap)
        print("滑动轨迹", track)
        slider = self.get_slider()
        self.move_to_gap(slider, track)
        if self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.m-text-cut"))):
            print('登录成功')
            time.sleep(100)
        else:
            print('登录失败')
        # if not sucess:
        #     self.crack()
        # else:
        #     self.login()

if __name__ == "__main__":
    crack = CrackGeetest()
    crack.crack()

