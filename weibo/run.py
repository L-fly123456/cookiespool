from weibo.crack import Crack
from weibo.click_carck import weibo_click
from weibo.slider_carck import CrackGeetest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class run(Crack):
    def __init__(self):
        Crack.__init__(self)
        self.go=weibo_click().main()
    def element(self):
        # self.go()
        # if self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_canvas_slice "))):
        #     crack = CrackGeetest()
        #     crack.crack()
        if self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_item_img "))):
            self.go()
        else:
            print('登录成功')

if __name__=="__main__":
    run().element()







