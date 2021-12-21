import logging
import time

import pytest
import yaml
from appium.webdriver.common.mobileby import MobileBy
from App.App import App


class Test_App():
    @pytest.fixture()
    def goto_login(self):
        self.loginPage = App().start().goto_loginPage()
        # pytest.assume(self.loginPage.find(MobileBy.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
        #                                                  "android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/"
        #                                                  "android.webkit.WebView/android.webkit.WebView/android.view.View[7]/android.view.View[2]").text == "登录")

    @pytest.mark.parametrize(('tenant,user,password'),
                             yaml.safe_load(open(r'D:\Software\JETBrainsPycharm\DocumentsDownload\Projects\CyberWaterGWAuto\Data\login.yaml', encoding='utf-8'))['loginDatasValuesTrue'])
    def test_login(self,tenant,user,password,goto_login):
        #pytest.assume()
        self.accountPasswordPage = self.loginPage.goto_accountPasswordPage()
        # self.accountPasswordPage.input_username_password(user, password)
        # self.accountPasswordPage.inputTenant(tenant)
        time.sleep(3)
        self.tenantPage = self.accountPasswordPage.goto_tenantPage()

        self.tenantPage.selectTenant("tenant")
        self.accountPasswordPage.input_username_password(user,password)
        self.mainPage = self.accountPasswordPage.goto_mainPage()
        time.sleep(10000)

    def test_GWWorkSheet(self):
        pass
    