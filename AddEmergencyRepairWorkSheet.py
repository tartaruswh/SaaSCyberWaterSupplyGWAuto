import time
#from typing import re

import pytesseract
import pytest
import yaml
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from BasePage import BasePage


class AddEmergencyRepairWorkSheet(BasePage):
    emergencyRepairWorkSheetName = ""
    def getEmergencyRepairWorkSheetName(self):
        return self.emergencyRepairWorkSheetName
    '''
    获取界面截图，判断元素位置
    '''
    def getPicturesLocation(self):
        self.cf_save_screenshot("./Pictures/location.png")
        page_obj = Image.open("./Pictures/location.png")
        img_loca = self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div[1]/span/button[1]")
        img_location = img_loca.location
        img_size = img_loca.size
        x_left = img_location["x"]+1000
        y_top = img_location["y"]+500
        x_right = x_left + img_size["width"]+500
        y_bottom = y_top + img_size["height"]+500
        img_obj = page_obj.crop((x_left, y_top, x_right, y_bottom))
        print(x_left,y_top,x_right,y_bottom)
        #img_obj.show()
        # pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\SoftwareInstallation\tesseract.exe"
        # result_imgToStr = pytesseract.image_to_string(img_obj)
        # num_str = re.findall(r"\d",result_imgToStr)
        # return "".join(num_str)
    '''
        新增抢维修工单必填项验证
        workSheetName: 输入的工单名称
        repairAddress：维修地点
        reportRepairTimeState：判断报修时间是否为空，用0、1判断，1不为空，0为空
        estimatedStartTimeState：判断预计开始时间是否为空，用0、1判断，1不为空，0为空
        executiveStaffState：判断执行人员状态是否为空，用0、1判断，1不为空，0为空
        chargePersonState：判断负责人状态是否为空，用0、1判断，1不为空，0为空
        teamState：
    '''
    #
    def emergencyRepairWorkSheetMandatoryContentTest(self):
        # 点击工单管理
        self.cf_find_ele(By.XPATH, "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span").click()
        self.cf_find_ele(By.XPATH, "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[5]/a/li/span")
        time.sleep(1)
        # 点击抢维修工单
        self.cf_find_ele(By.XPATH,
                         "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[5]/a/li/span").click()
        # 抢维修工单名称显示验证
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[1]/span[2]")
        # 抢维修工单名称验证
        pytest.assume(self.cf_find_ele(By.XPATH,
                                       "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[1]/span[2]").text == "抢维修工单")
        '''
            读取yaml测试参数数组的长度，对每个测试参数数据进行测试
            当必填项为非输入框时，参数数据以0进行校验，等于0时，则不进行填写操作
            
        '''
        with open('Data/emergencyRepair.yaml', encoding='utf-8') as f:
            x = yaml.safe_load(f)
            for i in range(len(x.get("mandatoryContent"))):
                #为1时，选择默认执行人员必填项验证
                if x.get("mandatoryContent")[i][6] == 1:
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,"//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span")
                    # 点击新增工单按钮
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                     "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span")
                    self.cf_find_ele(By.XPATH,
                                     "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span").click()
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                       "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/div/div/input")
                    #工单名称输入
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/div/div/input").send_keys(x.get("mandatoryContent")[i][0])
                    #维修地点输入
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[2]/div[1]/div/div/div/input").send_keys(x.get("mandatoryContent")[i][1])
                    if x.get("mandatoryContent")[i][2] == 0:
                        #点击报修时间
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/div/div/input").click()
                        for i in range(10):
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/div/div/input").send_keys(Keys.BACK_SPACE)
                        #清空时间后，点击报修时间按钮，清空时间选择插件
                        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/label").click()
                        # 选择执行人员
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                        '''
                                    获取执行人员下拉选择框下拉后的ul
                                    然后通过ul进行执行人员选项
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[6]/div[1]/div[1]/ul")
                        time.sleep(2)
                        UlworkSheetDeviceType.find_element_by_xpath("li[3]").click()
                        UlworkSheetDeviceType.find_element_by_xpath("li[2]").click()
                        # 选中执行人员后，点击执行人员关闭弹框
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/label").click()

                        # 选择负责人
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[2]/div/div/div/div").click()
                        '''
                                    获取执行人员下拉选择框下拉后的ul
                                    然后通过ul进行执行人员选项
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        #time.sleep(10000)
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        # 等待提示消息显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[8]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[8]/p").text == "有必填项未填写，请填好再提交！")
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())

                        self.cf_refresh()
                        continue
                    if x.get("mandatoryContent")[i][3] == 0:
                        #点击预计开始时间
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/div/div/input").click()
                        for i in range(20):
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/div/div/input").send_keys(Keys.BACK_SPACE)
                        #点击以及开始时间标题，清空时间选择插件
                        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/label").click()

                        # 选择执行人员
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                        '''
                                    获取执行人员下拉选择框下拉后的ul
                                    然后通过ul进行执行人员选项
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[6]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[3]").click()
                        UlworkSheetDeviceType.find_element_by_xpath("li[2]").click()
                        # 选中执行人员后，点击执行人员关闭弹框
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/label").click()

                        # 选择负责人
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[2]/div/div/div").click()
                        '''
                                    获取执行人员下拉选择框下拉后的ul
                                    然后通过ul进行执行人员选项
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        # 等待提示消息显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[8]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[8]/p").text == "有必填项未填写，请填好再提交！")
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())

                        self.cf_refresh()
                        continue
                    if x.get("mandatoryContent")[i][4] == 0:
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"/html/body/div[5]/p")
                        # 等待提示消息显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[5]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[5]/p").text == '[ "请选择班组或人员！" ]')
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())
                        self.cf_refresh()
                        continue
                    if x.get("mandatoryContent")[i][5] == 0:
                        # 选择执行人员
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                        '''
                                    获取执行人员下拉选择框下拉后的ul
                                    然后通过ul进行执行人员选项
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[5]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[3]").click()
                        UlworkSheetDeviceType.find_element_by_xpath("li[2]").click()
                        # 选中执行人员后，点击执行人员关闭弹框
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/label").click()
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        # 等待提示消息显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"/html/body/div[6]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[6]/p").text == "指定负责人不能为空！")
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())
                        self.cf_refresh()
                        continue

                    # 选择执行人员
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                    '''
                                获取执行人员下拉选择框下拉后的ul
                                然后通过ul进行执行人员选项
                            '''
                    UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[5]/div[1]/div[1]/ul")
                    time.sleep(1)
                    UlworkSheetDeviceType.find_element_by_xpath("li[3]").click()
                    UlworkSheetDeviceType.find_element_by_xpath("li[2]").click()
                    # 点击负责人
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[2]/div/div/div/div[1]/input").click()
                    '''
                                                        获取负责人下拉选择框下拉后的ul
                                                        然后通过ul进行负责人选项
                                                    '''
                    UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[6]/div[1]/div[1]/ul")
                    time.sleep(1)
                    UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                    # time.sleep(100)
                    # 选中执行人员后，点击执行人员关闭弹框
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/label").click()
                    self.cf_getTouchActions().scroll_from_element(
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                        0, 400).perform()
                    #点击保存按钮
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                    self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                    # 等待提示消息显示
                    self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[7]/p")
                    #验证消息提示弹框是否显示
                    pytest.assume(self.cf_find_ele(By.XPATH,"/html/body/div[7]/p").text == "有必填项未填写，请填好再提交！")
                    #新增工单界面是否显示
                    pytest.assume(self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[1]/span").is_displayed())
                    self.cf_refresh()
                    continue
                #为0时，选择默认执行班组必填项验证
                if x.get("mandatoryContent")[i][6] == 0:
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                       "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span")
                    # 点击新增工单按钮
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                       "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span")
                    self.cf_find_ele(By.XPATH,
                                     "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span").click()
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                       "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/div/div/input")
                    # 工单名称输入
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/div/div/input").send_keys(
                        x.get("mandatoryContent")[i][0])
                    # 维修地点输入
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[2]/div[1]/div/div/div/input").send_keys(
                        x.get("mandatoryContent")[i][1])
                    if x.get("mandatoryContent")[i][2] == 0:
                        # 点击报修时间
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/div/div/input").click()
                        for i in range(10):
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/div/div/input").send_keys(
                                Keys.BACK_SPACE)
                        # 清空时间后，点击报修时间按钮，清空时间选择插件
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/label").click()
                        # 点击启用班组按钮
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[7]/div/div").click()
                        # 班组下拉是否可点击
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div")
                        # 选择班组
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                        '''
                                    获取班组下拉选择框下拉后的ul
                                    然后通过ul进行班组选择 
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[6]/div[1]/div[1]/ul")
                        time.sleep(2)
                        UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                        # 选择负责人
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[2]/div/div/div/div").click()
                        '''
                                    获取班组下拉选择框下拉后的ul
                                    然后通过ul进行负责人选择 
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        # time.sleep(10000)
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        #等待提示消息显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"/html/body/div[8]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[8]/p").text == "有必填项未填写，请填好再提交！")
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())

                        self.cf_refresh()
                        continue
                    if x.get("mandatoryContent")[i][3] == 0:
                        # 点击预计开始时间
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/div/div/input").click()
                        for i in range(20):
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/div/div/input").send_keys(
                                Keys.BACK_SPACE)
                        # 点击以及开始时间标题，清空时间选择插件
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/label").click()
                        # 点击启用班组按钮
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[7]/div/div").click()
                        # 班组下拉是否可点击
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div")
                        # 选择班组
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                        '''
                                    获取班组下拉选择框下拉后的ul
                                    然后通过ul进行班组选择
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[6]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                        # 选择负责人
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[2]/div/div/div").click()
                        '''
                                    获取班组下拉选择框下拉后的ul
                                    然后通过ul进行负责人选择 
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        # 验证提示消息是否显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[8]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[8]/p").text == "有必填项未填写，请填好再提交！")
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())
                        self.cf_refresh()
                        continue
                    if x.get("mandatoryContent")[i][4] == 0:
                        # 点击启用班组按钮
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[7]/div/div").click()
                        # 班组下拉是否可点击
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div")
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[5]/p")
                        # 等待提示消息显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"/html/body/div[5]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[5]/p").text == '[ "请选择班组或人员！" ]')
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())
                        self.cf_refresh()
                        continue
                    if x.get("mandatoryContent")[i][5] == 0:
                        # 点击启用班组按钮
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[7]/div/div").click()
                        # 班组下拉是否可点击
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div")
                        # 选择班组
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                        '''
                                    获取班组下拉选择框下拉后的ul
                                    然后通过ul进行负责人选择 
                                '''
                        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[5]/div[1]/div[1]/ul")
                        time.sleep(1)
                        UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                        self.cf_getTouchActions().scroll_from_element(
                            self.cf_find_ele(By.XPATH,
                                             "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                            0, 400).perform()
                        # 点击保存按钮
                        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                           "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                        # 等待提示消息显示
                        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[6]/p")
                        # 验证消息提示弹框是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[6]/p").text == "指定负责人不能为空！")
                        # 新增工单界面是否显示
                        pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())
                        self.cf_refresh()
                        continue
                    #点击启用班组按钮
                    self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[7]/div/div").click()
                    #班组下拉是否可点击
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div")
                    # 选择班组
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/div/div").click()
                    '''
                                获取班组下拉选择框下拉后的ul
                                    然后通过ul进行负责人选择 
                            '''
                    UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[5]/div[1]/div[1]/ul")
                    time.sleep(1)
                    UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                    # 点击负责人
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[2]/div/div/div/div[1]/input").click()
                    '''
                                                        获取负责人下拉选择框下拉后的ul
                                                        然后通过ul进行负责人选项 
                                                    '''
                    UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[6]/div[1]/div[1]/ul")
                    time.sleep(1)
                    UlworkSheetDeviceType.find_element_by_xpath("li[1]").click()
                    # time.sleep(100)
                    # 选中执行人员后，点击执行人员关闭弹框
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[8]/div[1]/div/label").click()
                    self.cf_getTouchActions().scroll_from_element(
                        self.cf_find_ele(By.XPATH,
                                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
                        0, 400).perform()
                    # 点击保存按钮
                    self.cf_webDriverWaitUnitlIsEnable(By.XPATH,
                                                       "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]")
                    self.cf_find_ele(By.XPATH,
                                     "/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]").click()
                    self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"/html/body/div[7]/p")
                    # 等待提示消息显示
                    self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[7]/p")
                    # 验证消息提示弹框是否显示
                    pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[7]/p").text == "有必填项未填写，请填好再提交！")
                    # 新增工单界面是否显示
                    pytest.assume(self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[1]/span").is_displayed())
                    self.cf_refresh()
                    continue

    '''
        进行地图功能测试验证
    '''
    def mapTest(self):
        # 点击工单管理
        self.cf_find_ele(By.XPATH, "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span").click()
        self.cf_find_ele(By.XPATH, "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[5]/a/li/span")
        time.sleep(1)
        # 点击抢维修工单
        self.cf_find_ele(By.XPATH,
                         "//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[5]/a/li/span").click()
        # 抢维修工单名称显示验证
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,
                                              "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[1]/span[2]")
        # 点击新增工单按钮
        self.cf_find_ele(By.XPATH,
                         "//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span").click()
        #点击新建抢维修工单矩形拾取方式按钮
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div[1]/span/button[1]").click()
        self.cf_getActionChains().move_by_offset(200,200).click_and_hold().move_by_offset(400,400).release().perform()
        #判断结果详情列表是否显示
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div[4]/div[1]")
        #点击选中结果详情列表第一条设备
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div[4]/div[3]/div[3]/table/tbody/tr[1]/td[1]/div/label/span/span").click()
        time.sleep(10000)
    def addEmergencyRepairWorkSheetAllOptions(self):
        # 点击工单管理
        self.cf_find_ele(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span").click()
        self.cf_find_ele(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[5]/a/li/span")
        time.sleep(1)
        # 点击抢维修工单
        self.cf_find_ele(By.XPATH,"//*[@id='app']/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[5]/a/li/span").click()
        # 抢维修工单名称显示验证
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[1]/span[2]")
        # 抢维修工单名称验证
        pytest.assume(self.cf_find_ele(By.XPATH,"//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[1]/span[2]").text == "抢维修工单")
        # 点击新增工单按钮
        self.cf_find_ele(By.XPATH,"//*[@id='app']/div/div[3]/section/div/div[1]/div/div[2]/div/div[2]/button[1]/span").click()
        # 工单名称是否可编辑
        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/div/div[1]/input")
        # 获取当前时间
        currentTime = self.cf_getCurrentTime("%H:%M:%S %m-%d-%Y")
        # 要输入的抢维修工单名称
        self.emergencyRepairWorkSheetName = "Test抢维修工单" + currentTime
        # 工单名称输入
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/div/div[1]/input").send_keys(self.emergencyRepairWorkSheetName)
        time.sleep(1)
        # 获取工单级别下拉选择框的名称
        #print(self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[2]/div/label").text)
        # 点击工单级别下拉选择框
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[2]/div/div/div").click()
        '''
            获取工单级别下拉选择框下拉后的ul
            然后通过ul进行选中工单级别选项
        '''
        UlworkSheetLevel = self.cf_find_ele(By.XPATH, "/html/body/div[5]/div[1]/div[1]/ul")
        time.sleep(1)
        UlworkSheetLevel.find_element_by_xpath("li[3]").click()

        # 获取设备类型下拉选择框的名称
        #print(self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[3]/div/label").text)
        # 点击设备类型下拉选择框
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[3]/div/div/div").click()
        '''
            获取设备类型下拉选择框下拉后的ul
            然后通过ul进行选中设备类型选项
        '''
        UlworkSheetDeviceType = self.cf_find_ele(By.XPATH, "/html/body/div[6]/div[1]/div[1]/ul")
        time.sleep(1)
        UlworkSheetDeviceType.find_element_by_xpath("li[4]").click()
        #维修地点内容输入
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[2]/div[1]/div/div/div/input").send_keys("AutoTestRepairPlace")
        # 获取城区内工单下拉选择框的名称
        #print(self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[2]/div[2]/div/label").text)
        # 点击城区内工单下拉选择框
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[2]/div[2]/div/div/div").click()
        '''
            获取工单级别下拉选择框下拉后的ul
            然后通过ul进行选中工单级别选项
        '''
        UlworkSheetLevel = self.cf_find_ele(By.XPATH, "/html/body/div[7]/div[1]/div[1]/ul")
        time.sleep(1)
        UlworkSheetLevel.find_element_by_xpath("li[1]").click()
        time.sleep(1)
        #报修人名称输入
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[3]/div[1]/div/div/div/input").send_keys("ATestBXR")
        #联系方式输入
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[3]/div[2]/div/div/div/input").send_keys("18888888888")

        #先清空，然后再输入报修时间
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/div/div/input").clear()
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/div/div/input").send_keys(self.cf_getCurrentTime("%Y-%m-%d"))
        #点击报修时间字段，清空时间插件显示
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[4]/label").click()

        # 先清空，然后再输入预计开始时间
        self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/div/div/input").clear()
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/div/div/input").send_keys(self.cf_getCurrentTime("%Y-%m-%d %H:%M:%S"))
        # 点击预计开始时间字段，清空时间插件显示
        self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[5]/label").click()

        # 先清空，然后再输入预计完成时间
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[6]/div/div/input").send_keys(self.cf_getAppointTime("%Y-%m-%d %H:%M:%S",172800))
        # 点击预计完成时间字段，清空时间插件显示
        self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[6]/label").click()
        #点击启用班组
        self.cf_find_ele(By.XPATH,"//div[@class='el-switch']").click()
        self.cf_getTouchActions().scroll_from_element(
            self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[1]/div[1]/div/label"),
            0, 400).perform()
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"//div[@class='el-switch is-checked']/../../../div[8]/div[1]/div/div/div/div[1]/input[@ class = 'el-input__inner']")
        #点击执行班组
        self.cf_find_ele(By.XPATH,"//div[@class='el-switch is-checked']/../../../div[8]/div[1]/div/div/div/div[1]/input[@ class = 'el-input__inner']").click()
        '''
            获取执行班组下拉选择框下拉后的ul
            然后通过ul进行选中班组选项
        '''
        UlWorkSheetTeam = self.cf_find_ele(By.XPATH, "/html/body/div[11]/div[1]/div[1]/ul")
        time.sleep(2)
        UlWorkSheetTeam.find_element_by_xpath("li[1]").click()
        time.sleep(1)

        #点击指定负责人
        self.cf_find_ele(By.XPATH,"//div[@class='el-switch is-checked']/../../../div[8]/div[2]/div/div/div/div/input[@ class = 'el-input__inner']").click()

        '''
            获取指定负责人下拉选择框下拉后的ul
            然后通过ul进行选中负责人选项
        '''
        UlWorkSheetDirector = self.cf_find_ele(By.XPATH, "/html/body/div[12]/div[1]/div[1]/ul")
        time.sleep(1)
        UlWorkSheetDirector.find_element_by_xpath("li[1]").click()

        #问题描述
        self.cf_find_ele(By.XPATH,"//div[@class='el-switch is-checked']/../../../div[9]/div/div/textarea").send_keys("test")
        self.cf_getTouchActions().scroll_from_element(
            self.cf_find_ele(By.XPATH, "//div[@class='el-switch is-checked']/../../../div[9]/div/div/textarea"),0, 150).perform()

        #停水区域信息输入
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[11]/div/div/input").send_keys("test")
        #影响区域信息输入
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[12]/div/div/input").send_keys("test")
        #计划停水时间输入
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[13]/div/div/input").send_keys(self.cf_getAppointTime("%Y-%m-%d %H:%M:%S",172800))
        #点击计划停水时间，清空时间插件
        self.cf_find_ele(By.XPATH,
                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[13]/label").click()
        #预计修复时间
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[14]/div/div/input").send_keys(self.cf_getAppointTime("%Y-%m-%d %H:%M:%S",345600))
        #点击计划停水时间，清空时间插件
        self.cf_find_ele(By.XPATH,
                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[13]/label").click()
        #预计供水时间
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[15]/div/div/input").send_keys(self.cf_getAppointTime("%Y-%m-%d %H:%M:%S",518400))
        # 点击计划停水时间，清空时间插件
        self.cf_find_ele(By.XPATH,
                         "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[13]/label").click()
        #点击定额方案下拉选择框
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[17]/div/div/div[1]/input").click()
        '''
            获取额定下拉选择框下拉后的ul
            然后通过ul进行选中负责人选项
        '''
        time.sleep(2)
        UlWorkSheetDirector = self.cf_find_ele(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[17]/div/div/div[2]/div[1]/div[1]/ul")
        UlWorkSheetDirector.find_element_by_xpath("li[1]").click()
        #点击维修项目下拉选择框
        self.cf_webDriverWaitUnitlIsEnable(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[18]/div/div/div[1]/input")
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[18]/div/div/div[1]/input").click()
        '''
            获取维修项目选择框下拉后的ul
            然后通过ul进行选中负责人选项
        '''
        UlWorkSheetDirector = self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[18]/div/div/div[3]/div[1]/div[1]/ul")
        time.sleep(1)
        UlWorkSheetDirector.find_element_by_xpath("li[1]").click()
        UlWorkSheetDirector.find_element_by_xpath("li[2]").click()
        #点击维修项目清空维修项目插件显示
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[18]/label").click()
        #从维修项目开始滑动到底部
        self.cf_getTouchActions().scroll_from_element(self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/form/div[18]/label"),0,100).perform()
        #地图设备矩形类型获取
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div[1]/span/button[1]").click()
        self.cf_getActionChains().move_by_offset(200, 200).click_and_hold().move_by_offset(400, 400).release().perform()
        # 判断结果详情列表是否显示
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[4]")
        # 点击选中结果详情列表第一条设备
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[2]/div[4]/div[3]/div[3]/table/tbody/tr[1]/td[1]/div/label/span/span")
        self.cf_find_ele(By.XPATH,
                         "/html/body/div[2]/div/div[2]/div/div[2]/div[4]/div[3]/div[3]/table/tbody/tr[1]/td[1]/div/label/span/span").click()
        time.sleep(1)
        #点击保存按钮，完成工单创建
        self.cf_find_ele(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/section/main/div[3]/button[2]/span").click()
