import time

from selenium.webdriver.common.by import By

from AddEmergencyRepairWorkSheet import AddEmergencyRepairWorkSheet
from BasePage import BasePage
from LineTrackingWorkSheet import LineTrackingWorkSheet


class HomePage(BasePage):
    '''
        进入到抢维修工单界面，获取抢维修工单类对象实例，po原则方法
        :return 返回抢维修工单界面对象实例
    '''
    def goto_EmergenceRepairWorkSheet(self):

        return AddEmergencyRepairWorkSheet(self.driver)

    '''
        进入到巡线工单界面，获取巡线工单类对象实例，po原则方法
        :return 返回巡线工单界面对象实例
        '''
    def goto_LineTrackingWorkSheet(self):
        #点击工单管理
        self.cf_find_ele(By.XPATH, "")
        #点击巡线工单
        self.cf_find_ele(By.XPATH, "")
        return LineTrackingWorkSheet(self.driver)