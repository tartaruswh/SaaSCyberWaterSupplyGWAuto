import time

import pytest
from appium.webdriver.common.mobileby import MobileBy
from App.BasePage import BasePage


class TenantPage(BasePage):
    def selectTenant(self,tenant):
        time.sleep(2)
        self.change_to_webview()
        print(self.getDriver().current_context)
        print(self.getDriver().page_source)
        self.find(MobileBy.XPATH,
                  "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
                  "android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/"
                  "android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View/android.view.View/android.widget.EditText").send_keys("我可以啦")
        #租户输入框输入目标租户名称
        self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
                                 "android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.webkit.WebView/android.webkit.WebView/"
                                 "android.view.View[1]/android.view.View[1]/android.view.View[2]/android.view.View/android.view.View/android.widget.EditText").send_keys(tenant)
        #点击符合要求的第一个目标名称
        self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
                                 "android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/""android.webkit.WebView/android.webkit.WebView/android.view.View[2]/"
                                 "android.view.View/android.view.View/android.view.View/android.view.View").click()
        #等待选中后显示账号登录页输入框是否显示
        self.cf_webDriverWaitUnitlIsDisplayed(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
                                                             "android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/"
                                                             "android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View[1]/android.view.View/android.view.View/android.widget.EditText")
        #验证账号登录页输入框内容是否与目标租户名称一致
        pytest.assume(self.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/"
                                                             "android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/"
                                                             "android.webkit.WebView/android.webkit.WebView/android.view.View[4]/android.view.View[1]/android.view.View/android.view.View/android.widget.EditText").text == tenant)
