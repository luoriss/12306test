# -*- coding: utf-8 -*-
from pydoc import browse

from selenium.webdriver.common.by import By
from splinter.browser import Browser
from time import sleep
import traceback
import time, sys
import selenium
from selenium.webdriver.chrome.service import Service
from time import sleep
from Browser_manager.browser_init import Browser_driver


class Buying(object):
    driver_name = ''
    executable_path = ''
    #用户名，密码
    username = u"lhbe3328"
    passwd = u"lihui2003123223"
    #cookies
    starts = u"%u7126%u4F5C%2CJOF"
    ends = u"%u90D1%u5DDE%2CZZF"

    dtime = u"2024-11-3"
    # 车次，选择第几趟，0则从上之下依次点击
    order = 3
    ###乘客名
    users = [u"李辉"]
    ##席位
    xb = u"二等座"
    pz = u"成人票"

    """网址"""
    #选票网站
    ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
    #登录网址
    login_url = "https://kyfw.12306.cn/otn/resources/login.html"
    #个人中心
    initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
    #购票网址
    buy = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"

    def __init__(self):
        self.driver_name = 'chrome'
        self.executable_path = r"C:\Users\hui\.wdm\drivers\chromedriver\win64\109.0.5414.74\chromedriver.exe"

    def login(self):
        driver=Browser_driver().Browser_init()
        driver.get(self.login_url)
        #self.driver.visit(self.login_url)
        self.driver.find_element(By.ID, "J-userName").sendkeys(self.username)
        #self.driver.fill("J—userName", self.username)
        # sleep(1)
        self.driver.find_element(By.ID, "J-password").sendkeys(self.passwd)
        #self.driver.fill("J-password", self.passwd)
        print(u"等待验证码��自行输入...")
        while True:
            if self.driver.url != self.initmy_url:
                sleep(1)
            else:
                break
#重新放入cookies
    def reload(self):
        self.driver.reload()
        self.driver.cookies.add({"_jc_save_fromStation": self.starts})
        self.driver.cookies.add({"_jc_save_toStation": self.ends})
        self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
        self.driver.reload()
#开始购票
    def start(self):
        service = Service(executable_path=self.executable_path)
        self.driver = Browser(driver_name=self.driver_name, service=service)
        self.driver.driver.set_window_size(1400, 1000)
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print("购票页面开始")
            # sleep(1)
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})

            self.driver.reload()

            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text(u"查询").click()
                    count += 1
                    print(u"循环点击查询... 第 %s 次" % count)
                    # sleep(1)
                    try:
                        self.driver.find_by_text(u"预订")[self.order - 1].click()
                    except Exception as e:
                        print(e)
                        print(u"还没开始预订")
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text(u"查询").click()
                    count += 1
                    print(u"循环点击查询... 第 %s 次" % count)
                    #sleep(0.8)
                    try:
                        for i in self.driver.find_by_text(u"预订"):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print(u"还没开始预订 %s" % count)
                        continue
            print(u"开始预订...")
            # sleep(3)
            # self.driver.reload()
            sleep(1)
            print(u'开始选择用户...')
            for user in self.users:
                self.driver.find_by_text(user).last.click()

            print(u"提交订单...")
            sleep(1)
            self.driver.find_by_text(self.pz).click()
            self.driver.find_by_id('').select(self.pz)
            # sleep(1)
            self.driver.find_by_text(self.xb).click()
            sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            print(u"开始选座...")
            self.driver.find_by_id('1D').last.click()
            self.driver.find_by_id('1F').last.click()

            sleep(1.5)
            print(u"确认选座...")
            self.driver.find_by_id('qr_submit_id').click()

        except Exception as e:
            print(e)
            
            


if __name__ == '__main__':
    Buying = Buying()
    Buying.start()

