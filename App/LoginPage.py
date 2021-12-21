import time

import pytest
from appium.webdriver.common.mobileby import MobileBy

from App.AccountPasswordPage import AccountPasswordPage
from App.BasePage import BasePage


class LoginPage(BasePage):
    #点击账号密码吗登录按钮，跳转到账号密码登录界面
    def goto_accountPasswordPage(self):
        time.sleep(2)
        #点击账号密码登录按钮，跳转到账号密码登录界面
        self.find(MobileBy.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/'
                                 'android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[8]').click()
        #time.sleep(2)
        # # 等待账号密码登录界面"公司"名称显示
        # self.cf_webDriverWaitUnitlIsDisplayed(MobileBy.XPATH,
        #                                       "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
        #                                       "android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[3]")
        # 验证账号密码登录界面“公司”名称是否显示正确
        # pytest.assume(self.find(MobileBy.XPATH,
        #                         "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
        #                         "android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[3]").text == "公司")
        return AccountPasswordPage(self.getDriver())

