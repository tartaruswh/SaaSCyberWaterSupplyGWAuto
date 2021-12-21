import logging

from appium.webdriver.webdriver import WebDriver
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

'''
    packageName:com.bewgcloud.ws.saas
    loginSuccessActivity:io.dcloud.PandoraEntryActivity
'''

class BasePage():
    logging.basicConfig(level=logging.INFO)
    # 定义了一个
    _black_list = [
        (By.XPATH, "//*[@text='允许']")
    ]
    # 定义查找黑名单的初始尝试次数
    _error_time = 0

    # 定义了查找黑名单的最多尝试测试
    _error_max_time = 3

    # 定义步骤驱动中，send的value的值
    _param = {}

    #初始化为空的driver
    def __init__(self,driver:WebDriver=None):
        if driver == None:
            '''
            #华为手机 PQY0220B05008165
            "deviceName": "PQY0220B05008165",
            #nova 手机
            "deviceName": "JPFDU19114002097",
            #红米 手机
            "deviceName": "d0ac8f56", Activity
            #网易木木模拟器
            "deviceName": "127.0.0.1:7555",
            #夜深模拟器
            "deviceName": "127.0.0.1:59865",
            #AS模拟器
            "deviceName": "emulator-5554",
            '''
            self.xueqiu_desire_cap = {
                "platformName": "android",
                "platformVersion": "11",
                # 夜深模拟器
                "deviceName": "127.0.0.1:59865",
                # "noReset": "true",
                "appPackage": "com.xueqiu.android",
                "appActivity": ".view.WelcomeActivityAlias",
                "autoGrantPermissions": True,
                "chromedriverExecutable": r"D:\test\chromedriverHybrid"
            }
            self.xueqiu_meizu_desire_cap = {
                "platformName": "android",
                "platformVersion": "8",
                # meizu16p
                "deviceName": "892QAETGAT958",
                # "noReset": "true",
                # "appPackage": "com.xueqiu.android",
                # "appActivity": ".view.WelcomeActivityAlias",
                "appPackage": "com.bewgcloud.ws.saas",
                "appActivity": "io.dcloud.PandoraEntry",
                "autoGrantPermissions": True,
                "chromedriverExecutable": r"D:\test\chromedriverHybrid"
            }
            self.oppo_desire_cap = {
                "platformName": "android",
                "platformVersion": "11",
                "deviceName": "9c87d2a4",
                "noReset": "true",
                "appPackage": "com.bewgcloud.ws.saas",
                "appActivity": "io.dcloud.PandoraEntry",
                "autoGrantPermissions": True,
                "chromedriverExecutable": r"D:\test\chromedriverOppo\chromedriver.exe"
            }
            self.AS_desire_cap = {
                "platformName": "android",
                "platformVersion": "6",
                # AS模拟器
                "deviceName": "emulator-5554",
                "noReset": "true",
                "appPackage": "com.bewgcloud.ws.saas",
                "appActivity": "io.dcloud.PandoraEntry",
                "autoGrantPermissions": True,
                "chromedriverExecutable": r"D:\test\chromedriverHybrid\chromedriver.exe"
            }
            self.Genymotion_desire_cap = {
                "platformName": "android",
                "platformVersion": "6",
                "deviceName": "192.168.63.104:5555",
                "noReset": "true",
                # "appPackage": "com.xueqiu.android",
                # "appActivity": ".view.WelcomeActivityAlias",
                "appPackage": "com.bewgcloud.ws.saas",
                "appActivity": "io.dcloud.PandoraEntry",
                "autoGrantPermissions": True,
                "chromedriverExecutable": r"D:\test\chromedriverGenymotion\chromedriver.exe"
            }
            self._driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.Genymotion_desire_cap)
            # self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", self.Genymotion_desire_cap)
            self._driver.implicitly_wait(5)
        if driver != None:
            self._driver = driver

    #返回driver对象
    def getDriver(self):
        return self._driver

    #封装find_element的函数，具备查找弹框的处理机制
    def find(self,locator,value):
        #通过log日志打印出要传的locator和value
        logging.info(locator)
        logging.info(value)

        # if isinstance(locator,tuple):
        #     return self._driver.find_element(*locator)
        # else:
        #     return self._driver.find_element(locator,value)
        # 把上面的变成一个三元的表达式

        try:
            #这里是一个三元的传值，里面的locator可以写成(By.ID,"id")或者By.ID,"id"两者都行
            return self._driver.find_element(*locator) if isinstance(locator,tuple) else self._driver.find_element(locator,value)
        #把异常定义为e
        except Exception as e:
            #当尝试的次数大于最大的尝试次数，就报错，不让这个try死循环
            if self._error_time > self._error_max_time:
                raise e
            #当尝试一次，尝试查找弹窗次数+1
            self._error_time+=1
            #循环遍历黑名单的locator
            for ele in self._black_list:
                #查找黑名单的元素
                black_elements=self._driver.find_elements(*ele)
                #当元素的值大于1，表示找到了黑名单弹窗的元素
                if len(black_elements) > 0:
                    #就点击一下，让弹窗消失
                    black_elements[0].click()
                    #由于弹窗消失了，所以可以找到元素了，调用自己
                    self.find(locator,value)
            #找不到元素就抛出异常
            raise e

    # 切换至webview
    def change_to_webview(self):
        self._driver.switch_to.context(self._driver.contexts[-1])

    # 切换至native
    def change_to_native(self):

        self._driver.switch_to.context(self._driver.contexts[0])
    '''
        封装的显示等待方法，until直到元素可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlIsDisplayed(self,by:By,locator:str,timeout:float = 10):
        webDriverWait:WebDriverWait = WebDriverWait(self._driver,timeout).until(lambda x:self.find(by,locator).is_displayed())
        return webDriverWait
    '''
        封装的显示等待方法，untilNot直到元素不可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlNotIsDisplayed(self,by:By,locator:str,timeout:float = 10):
        webDriverWaitNot:WebDriverWait = WebDriverWait(self._driver,timeout).until_not(lambda x:self.find(by,locator).is_displayed())
        return webDriverWaitNot

    '''
        封装的显示等待方法，until直到元素可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlIsEnable(self,by:By,locator:str,timeout:float = 10):
        webDriverWait:WebDriverWait = WebDriverWait(self._driver,timeout).until(lambda x:self.find(by,locator).is_enabled())
        return webDriverWait
    '''
        封装的显示等待方法，untilNot直到元素不可以获取
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''
    def cf_webDriverWaitUnitlNotIsEnable(self,by:By,locator:str,timeout:float = 10):
        webDriverWaitNot:WebDriverWait = WebDriverWait(self._driver,timeout).until_not(lambda x:self.find(by,locator).is_enabled())
        return webDriverWaitNot

    '''
            封装的显示等待方法，until直到元素可以选择
            by：By类型，设置获取参数的方式xpath、css、id、name等
            locator：获取元素方式的具体数值
            timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
        '''

    def cf_webDriverWaitUnitlIsSelected(self, by: By, locator: str, timeout: float = 10):
        webDriverWait: WebDriverWait = WebDriverWait(self._driver, timeout).until(
            lambda x: self.find(by, locator).is_selected())
        return webDriverWait

    '''
        封装的显示等待方法，untilNot直到元素不可以选择
        by：By类型，设置获取参数的方式xpath、css、id、name等
        locator：获取元素方式的具体数值  
        timeout：设置的显示等待工作时间，默认十秒，超过十秒为获取，自动失败
    '''

    def cf_webDriverWaitUnitlNotIsSelected(self, by: By, locator: str, timeout: float = 10):
        webDriverWaitNot: WebDriverWait = WebDriverWait(self._driver, timeout).until_not(
            lambda x: self.find(by, locator).is_selected())
        return webDriverWaitNot