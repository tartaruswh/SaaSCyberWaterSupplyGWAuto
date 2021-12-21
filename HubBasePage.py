# import logging
# import os
#
# from selenium import webdriver
# '''
# 基类：
# 1、单例模式封装driver
# 2、因调用driver封装元素获取方法
# 3、因调用driver显示等待封装
# '''
#
# class BasePage():
#     driver:webdriver
#     base_url = ""
#     def __init__(self,driver:webdriver = None,browserName = None):
#         logging.info("basePage")
#         #浏览器优先判断：
#         # if browserName == None:
#         #     self.driver = driver
#         if driver == None:
#             self.driver = webdriver.Remote("http://192.168.199.1:4444/wd/hub", chromeCaps=self.getChromeCaps(),
#                                        options=self.getChromeOptions())
#             self.driver.get("https://ws-test.cyberwater.com")
#         # if browserName == "chrome":
#         #     if driver == None:
#         #         self.driver = webdriver.Remote("http://192.168.199.1:4444/wd/hub", chromeCaps=self.getChromeCaps(),
#         #                                        options=self.getChromeOptions())
#         #     if driver != None:
#         #         self.driver = driver
#         #
#         # if browserName == "firefox":
#         #     if driver == None:
#         #         self.driver = webdriver.Remote("http://192.168.199.1:4444/wd/hub",firefoxCaps = self.getFirefoxCaps(),
#         #                                        browser_profile=self.getFirefoxProfile())
#         if driver != None:
#             self.driver = driver
#
#
#
#         if self.base_url != "":
#             self.driver.get(self.base_url)
#
#     def cf_find_ele(self,by,locator):
#         return self.driver.find_element(by,locator)
#
#     def cf_find_eles(self,by,locator):
#         return self.driver.find_elements(by,locator)
#
#     def cf_back(self):
#         return self.driver.back()
#
#     def getChromeCaps(self):
#         chromeCaps = {}
#         chromeCaps["browserName"] = "chrome"
#         # caps["browserName"] = os.getenv('browserName',None)
#         chromeCaps["platform"] = "WINDOWS"
#         chromeCaps["javascriptEnabled"] = True
#         return chromeCaps
#     def getChromeOptions(self):
#         chromeOptions = webdriver.ChromeOptions()
#         chromeOptions.add_argument('--ignore-certificate-errors')
#         return chromeOptions
#
#     def getFirefoxCaps(self):
#         firefoxCaps = {}
#         firefoxCaps["browserName"] = "firefox"
#         # caps["browserName"] = os.getenv('browserName',None)
#         firefoxCaps["platform"] = "WINDOWS"
#         firefoxCaps["javascriptEnabled"] = True
#         return firefoxCaps
#     def getFirefoxProfile(self):
#         firefoxProfile = webdriver.FirefoxProfile()
#         firefoxProfile.accept_untrusted_certs = True
#         return firefoxProfile