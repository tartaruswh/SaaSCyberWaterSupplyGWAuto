import logging
import time

from selenium import webdriver
from selenium.webdriver import TouchActions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

'''
基类：
1、单例模式封装driver
2、因调用driver封装元素获取方法
3、因调用driver显示等待封装
'''

class BasePage():
    driver:webdriver
    base_url = "https://ws-test.cyberwater.com"
    #base_url = "https://ws-uat.cyberwater.com/"
    '''
        初始化方法，单例模式获取driver实例，获取对象地址、
        driver：webdriver参数
    '''
    def __init__(self,driver:webdriver = None):
        if driver == None:
            self.driver = webdriver.Chrome(desired_capabilities=self.getChromeCaps(),options=self.getChromeOptions())
        if driver != None:
            self.driver = driver
        if self.base_url != "":
            self.driver.get(self.base_url)
    '''
        封装获取单个元素的方法
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
    '''
    def cf_find_ele(self,by:By,locator:str):
        return self.driver.find_element(by,locator)
    '''
        封装同时获取多个元素的方法
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
    '''
    def cf_find_eles(self,by:By,locator:str):
        return self.driver.find_elements(by,locator)
    '''
        封装的返回方法，调用自动执行返回操作
    '''
    def cf_back(self):
        return self.driver.back()
    '''
        封装的窗口最大化方法
    '''
    def cf_maximize_window(self):
        self.driver.maximize_window()
    '''
        封装的获取driver的方法，不对外暴漏driver实例
    '''
    def cf_getDriver(self):
        return self.driver
    '''
        封装的截屏方法
        path：截图后保存的路径
    '''
    def cf_save_screenshot(self,path:str):
        self.driver.save_screenshot(path)

    '''
        获取当前时间，并返回格式为 %H:%M:%S %m-%d-%Y 
    '''
    def cf_getCurrentTime(self,format):
        #%H:%M:%S %m-%d-%Y
        currentTime = time.strftime(format)
        # 要输入的抢维修工单名称
        return currentTime

    '''
        获取当前时间，并返回指定格式
        format:指定时间格式
        seconds:指定时间改动范围，减少或增加时间  
        :return 返回时间结果 
    '''
    def cf_getAppointTime(self, format,seonds):
        # %H:%M:%S %m-%d-%Y
        appoiintTime = time.strftime(format, time.localtime(time.time() + seonds))
        # 要输入的抢维修工单名称
        return appoiintTime

    '''
        获取滑动对象TouchActions
        :return 返回touchActions对象  
    '''
    def cf_getTouchActions(self):
        touchActions = TouchActions(self.driver)
        return touchActions

    '''
        获取滑动对象actionChains
        :return 返回actionsChains对象  
    '''

    def cf_getActionChains(self):
        actionsChains = ActionChains(self.driver)
        return actionsChains

    '''
        刷新界面操作
    '''
    def cf_refresh(self):
        self.driver.refresh()
    '''
        封装的显示等待方法，until直到元素可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlIsDisplayed(self,by:By,locator:str,timeout:float = 10):
        webDriverWait:WebDriverWait = WebDriverWait(self.driver,timeout).until(lambda x:self.cf_find_ele(by,locator).is_displayed())
        return webDriverWait
    '''
        封装的显示等待方法，untilNot直到元素不可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlNotIsDisplayed(self,by:By,locator:str,timeout:float = 10):
        webDriverWaitNot:WebDriverWait = WebDriverWait(self.driver,timeout).until_not(lambda x:self.cf_find_ele(by,locator).is_displayed())
        return webDriverWaitNot

    '''
        封装的显示等待方法，until直到元素可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlIsEnable(self,by:By,locator:str,timeout:float = 10):
        webDriverWait:WebDriverWait = WebDriverWait(self.driver,timeout).until(lambda x:self.cf_find_ele(by,locator).is_enabled())
        return webDriverWait
    '''
        封装的显示等待方法，untilNot直到元素不可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlNotIsEnable(self,by:By,locator:str,timeout:float = 10):
        webDriverWaitNot:WebDriverWait = WebDriverWait(self.driver,timeout).until_not(lambda x:self.cf_find_ele(by,locator).is_enabled())
        return webDriverWaitNot

    '''
            封装的显示等待方法，until直到元素可以选择
            by：By类型，设置获取参数的方式xpath、css、id、name等
            locator：获取元素方式的具体数值
            timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
        '''

    def cf_webDriverWaitUnitlIsSelected(self, by: By, locator: str, timeout: float = 10):
        webDriverWait: WebDriverWait = WebDriverWait(self.driver, timeout).until(
            lambda x: self.cf_find_ele(by, locator).is_selected())
        return webDriverWait

    '''
        封装的显示等待方法，untilNot直到元素不可以选择
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''

    def cf_webDriverWaitUnitlNotIsSelected(self, by: By, locator: str, timeout: float = 10):
        webDriverWaitNot: WebDriverWait = WebDriverWait(self.driver, timeout).until_not(
            lambda x: self.cf_find_ele(by, locator).is_selected())
        return webDriverWaitNot

    '''
        desired_capabilities数据参数key对应的值，webdriver.Chrome()中的参数
    '''
    def getChromeCaps(self):
        chromeCaps = {}
        chromeCaps["browserName"] = "chrome"
        chromeCaps["platform"] = "WINDOWS"
        chromeCaps["javascriptEnabled"] = True
        return chromeCaps
    '''
        options数据参数key对应的值，webdriver.Chrome()中的参数
    '''
    def getChromeOptions(self):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--ignore-certificate-errors')
        chromeOptions.add_experimental_option('w3c',False)
        return chromeOptions

    '''
        desired_capabilities数据参数key对应的值，webdriver.Firefox()中的参数
    '''
    def getFirefoxCaps(self):
        firefoxCaps = {}
        firefoxCaps["browserName"] = "firefox"
        # caps["browserName"] = os.getenv('browserName',None)
        firefoxCaps["platform"] = "WINDOWS"
        firefoxCaps["javascriptEnabled"] = True
        return firefoxCaps

    '''
        options数据参数key对应的值，webdriver.Firefox()中的参数
    '''
    def getFirefoxProfile(self):
        firefoxProfile = webdriver.FirefoxProfile()
        firefoxProfile.accept_untrusted_certs = True
        return firefoxProfile