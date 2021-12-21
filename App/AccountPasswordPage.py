import time

import pytest
from appium.webdriver.common.mobileby import MobileBy

from App.BasePage import BasePage
from App.MainPage import MainPage
from App.TenantPage import TenantPage


class AccountPasswordPage(BasePage):
    # 点击租户输入框，跳转到租户选择界面，进行租户搜索
    # /html/body/div[1]/uni-view/uni-view[1]/uni-view/uni-view[1]/uni-input/div
    def goto_tenantPage(self):
        self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
                                 "android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/"
                                 "android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View[1]").click()
        #self.cf_webDriverWaitUnitlIsDisplayed(MobileBy.XPATH,"/html/body/div[1]/uni-view/uni-view[2]")
        #pytest.assume(self.find(MobileBy.XPATH,"/html/body/div[1]/uni-view/uni-view[2]").text == "取消")
        return TenantPage(self.getDriver())
    # 输入用户名与密码
    def input_username_password(self,username,password):
        #点击用户名输入框，输入用户名称
        self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                 "android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/"
                                 "android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[6]/android.view.View[1]/"
                                 "android.view.View/android.view.View/android.widget.EditText").send_keys(username)
        #点击密码输入框，输入密码
        self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                 "android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/"
                                 "android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[8]/android.view.View[1]/"
                                 "android.view.View[1]/android.view.View/android.widget.EditText").send_keys(password)

    #点击登录
    def goto_mainPage(self):
        self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                                 "android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/"
                                 "android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[11]/android.view.View[2]").click()
        return MainPage(self.getDriver())

    def inputTenant(self,tenant):
        self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View[1]/android.view.View/android.view.View/android.widget.EditText").send_keys(tenant)