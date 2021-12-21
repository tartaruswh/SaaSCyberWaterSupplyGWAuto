import pytest
from appium import webdriver
#这是app的类，负责启动，关闭，重启等操作
from appium.webdriver.common.mobileby import MobileBy

from App.BasePage import BasePage
from App.LoginPage import LoginPage


class App(BasePage):

    #启动app
    def start(self):
        return self

    def stop(self):
        pass

    def restart(self):
        return self

    #获取loginPage的对象方法
    def goto_loginPage(self):
        #回去loginPage对象
        return LoginPage(self.getDriver())
