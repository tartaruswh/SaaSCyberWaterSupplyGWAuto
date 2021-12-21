import logging
import time
import threading
import pytest
import yaml
from selenium.webdriver.common.by import By
from BasePage import BasePage
from LoginPage import LoginPage


class TestRun():
    '''
        使用fixture声明进行类似setup与teardown的准备操作
        声明初始页面类对象，用于登录测试的导入，需每次结束后退出
    '''
    loginPage:LoginPage
    @pytest.fixture()
    def loginPage_ready(self):
        self.loginPage = LoginPage()
        yield
        time.sleep(2)
        self.loginPage.cf_getDriver().quit()
    '''
                登录成功的方法 
                参数实例化：parametrize，获取参数内容
                tenant：yaml中的租户
                user：yaml中的用户
                password：yaml中的密码
                start_ready:调用的fixture声明函数
                assert：验证登录成功后，进入到主页获取个人中心信息  
            '''

    @pytest.mark.parametrize(('tenant,user,password'),
                             yaml.safe_load(open('./Data/login.yaml', encoding='utf-8'))['loginDatasValuesTrue'])
    @pytest.fixture()
    def login(self, tenant, user, password, loginPage_ready):
        self.loginPage.cf_maximize_window()
        # 显示等待获取验证码元素
        self.loginPage.cf_webDriverWaitUnitlIsDisplayed(By.NAME, "verifyCode")
        self.CAPTCHA = self.loginPage.getCAPTCHA()
        self.loginPage.inputAccount(tenant, user, password, self.CAPTCHA)
        # 点击登录按钮，获取home对象实例
        self.loginPage.cf_find_ele(By.XPATH, "//*[@id='pane-first']/form/div[6]/button").click()
        self.homePage = self.loginPage.goto_HomePage()
        # 显示等待获取个人中心
        self.homePage.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,
                                                       "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[3]/li/div")
        # 获取个人中心
        pytest.assume(self.homePage.cf_find_ele(By.XPATH,
                                                "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[3]/li/div").is_displayed())
    '''
        测试账号密码输入登录失败的方法
        参数实例化：parametrize，获取参数内容
        tenant：yaml中的租户
        user：yaml中的用户
        password：yaml中的密码
        start_ready:调用的fixture声明函数  
        assert：验证登录失败后，登录按钮可获取
    '''
    @pytest.mark.skip(reason = "跳过验证")
    @pytest.mark.parametrize(('tenant,user,password'),yaml.safe_load(open('./Data/login.yaml', encoding='utf-8'))['loginDatasValuesFalse'])
    def test_input(self,tenant,user,password,loginPage_ready):
        self.loginPage.cf_maximize_window()
        self.CAPTCHA = self.loginPage.getCAPTCHA()
        self.loginPage.inputAccount(tenant, user, password, self.CAPTCHA)
        # 点击登录按钮，获取home对象实例
        self.loginPage.cf_find_ele(By.XPATH, "//*[@id='pane-first']/form/div[6]/button").click()
        #获取登录按钮元素
        assert self.loginPage.cf_find_ele(By.XPATH,"//*[@id='pane-first']/form/div[6]/button").is_displayed()


    '''
        测试登录成功的方法 
        参数实例化：parametrize，获取参数内容
        tenant：yaml中的租户
        user：yaml中的用户
        password：yaml中的密码
        start_ready:调用的fixture声明函数
        assert：验证登录成功后，进入到主页获取个人中心信息  
    '''
    @pytest.mark.parametrize(('tenant,user,password'),yaml.safe_load(open('./Data/login.yaml', encoding='utf-8'))['loginDatasValuesTrue'])
    def test_login(self,tenant,user,password,loginPage_ready):
        self.loginPage.cf_maximize_window()
        #显示等待获取验证码元素
        self.loginPage.cf_webDriverWaitUnitlIsDisplayed(By.NAME,"verifyCode")
        self.CAPTCHA = self.loginPage.getCAPTCHA()
        self.loginPage.inputAccount(tenant, user, password, self.CAPTCHA)
        #点击登录按钮
        self.loginPage.clickLoginButton("//*[@id='pane-first']/form/div[6]/button")
        self.homePage = self.loginPage.goto_HomePage()
        #显示等待获取个人中心
        self.homePage.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[3]/li/div")
        #获取个人中心
        pytest.assume(self.homePage.cf_find_ele(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[3]/li/div").is_displayed())

    '''
        测试新增抢维修工单界面  
    '''

    @pytest.mark.parametrize(('tenant,user,password'),yaml.safe_load(open('./Data/login.yaml', encoding='utf-8'))['loginDatasValuesTrue'])
    def test_addEmergencyRepairWorkSheetAllInfo(self,loginPage_ready,login):
        time.sleep(1)
        # 抢维修工单点击准备
        self.addEmergencyRepairWorkSheet = self.homePage.goto_EmergenceRepairWorkSheet()
        self.addEmergencyRepairWorkSheet.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span")
        self.addEmergencyRepairWorkSheet.addEmergencyRepairWorkSheetAllOptions()
        #验证点击保存后，是否返回homePage，验证抢维修工单标题是否显示
        self.homePage.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[1]/span[2]")
        time.sleep(3)
        self.homePage.cf_refresh()
        # 验证点击保存后，是否返回homePage，验证抢维修工单标题是否显示
        self.homePage.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,
                                                       "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[1]/span[2]")
        #验证新增界面工单是否显示到homePage抢维修工单列表
        pytest.assume(self.homePage.cf_find_ele(By.XPATH,"//*[@id='app']/div/div[3]/section/div/div[1]/div/div[3]/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[3]/div/div/div").text
                      == self.addEmergencyRepairWorkSheet.getEmergencyRepairWorkSheetName())

    '''
        抢维修新建工单必填项功能测试 
    '''

    @pytest.mark.parametrize(('tenant,user,password'),
                             yaml.safe_load(open('./Data/login.yaml', encoding='utf-8'))['loginDatasValuesTrue'])
    def test_addERWorkSheetMandatoryContent(self,loginPage_ready,login):
        time.sleep(1)
        # 抢维修工单点击准备
        self.addEmergencyRepairWorkSheet = self.homePage.goto_EmergenceRepairWorkSheet()
        self.addEmergencyRepairWorkSheet.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span")
        time.sleep(2)
        self.addEmergencyRepairWorkSheet.emergencyRepairWorkSheetMandatoryContentTest()

    @pytest.mark.parametrize(('tenant,user,password'),
                             yaml.safe_load(open('./Data/login.yaml', encoding='utf-8'))['loginDatasValuesTrue'])
    def test_emergencyRepairWorkSheetMapTest(self,loginPage_ready,login):
        time.sleep(1)
        # 抢维修工单点击准备 
        self.addEmergencyRepairWorkSheet = self.homePage.goto_EmergenceRepairWorkSheet()
        self.addEmergencyRepairWorkSheet.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,
                                                                          "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span")
        self.addEmergencyRepairWorkSheet.mapTest()

    @pytest.mark.parametrize(('tenant,user,password'),
                             yaml.safe_load(open('./Data/login.yaml', encoding='utf-8'))['loginDatasValuesTrue'])
    @pytest.mark.parametrize(('a,b,c'),
                             yaml.safe_load(open('./Data/test.yaml', encoding='utf-8'))['test1'])
    def test_mustLogintest(self,a,b,c,loginPage_ready,login):

        print(a,b,c)
        with open('Data/emergencyRepair.yaml', encoding='utf-8') as f:
            x = yaml.safe_load(f)
            for i in range(len(x.get("mandatoryContent"))):
                print(x.get("mandatoryContent")[i][0])
                print(x.get("mandatoryContent")[i][1])
                print(x.get("mandatoryContent")[i][2])
                print(x.get("mandatoryContent")[i][3])
                print(x.get("mandatoryContent")[i][4])
                print(x.get("mandatoryContent")[i][5])
        pass
    def test_2(self):
        pytest.assume(1 == 1 )