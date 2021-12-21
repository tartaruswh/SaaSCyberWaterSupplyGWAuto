import re
import time

import pytest
from selenium import webdriver
from PIL import Image
from HomePage import HomePage
from selenium.webdriver.common.by import By
from BasePage import BasePage
import pytesseract

class LoginPage(BasePage):
    '''
        登录界面租户、用户、密码、验证码数据输入的方法
        :tenant：租户名
        :userName：用户名
        :password：密码
        :CAPTCHA：验证码
    '''
    def inputAccount(self,tenant,userName,password,CAPTCHA):
        #time.sleep(8)
        self.cf_webDriverWaitUnitlIsDisplayed(By.XPATH,"//*[@id='pane-first']/form/div[1]/div/div/input")
        self.cf_find_ele(By.XPATH,
                         "//*[@id='pane-first']/form/div[1]/div/div/input").click()
        self.cf_find_ele(By.XPATH,"//*[@id='pane-first']/form/div[1]/div/div/input").send_keys(tenant)
        self.cf_find_ele(By.XPATH, "//*[@id='pane-first']/form/div[2]/div/div/input").click()
        self.cf_find_ele(By.XPATH, "//*[@id='pane-first']/form/div[2]/div/div/input").send_keys(userName)
        self.cf_find_ele(By.XPATH, "//*[@id='pane-first']/form/div[3]/div/div/input").click()
        self.cf_find_ele(By.XPATH, "//*[@id='pane-first']/form/div[3]/div/div/input").send_keys(password)
        self.cf_find_ele(By.NAME,"verifyCode").send_keys(CAPTCHA)

    '''
        登录成功后，进入到主页面，获取主页类对象实例，po原则方法
        :return 返回主页实例，传入当前的driver
    '''
    def goto_HomePage(self):
        time.sleep(3)
        return HomePage(self.driver)

    def clickLoginButton(self,locator:str):
        # 点击登录按钮，获取home对象实例
        self.cf_find_ele(By.XPATH,locator).click()

    '''
        获取验证码方法：
            1、进行截图后，使用image类进行图片处理准备
            2、点击验证码，获取验证码的位置信息
            3、根据位置信息，进行验证码范围的获取
            4、获取验证码位置范围后，在截图中进行裁剪，验证码最终截取范围是左上角x，y坐标与右下角x，y坐标  
            5、使用pytesseracet工具对裁剪后的图片内容进行转换为字符串格式  
            6、将字符串格式更改为验证码数字数组格式，再转换为字符串
            :return 返回验证码字符串   
    '''
    def getCAPTCHA(self):
        self.cf_save_screenshot("./Pictures/CAPTCHA.png")
        page_obj = Image.open("./Pictures/CAPTCHA.png")
        img_loca = self.cf_find_ele(By.NAME, "verifyCode")
        img_location = img_loca.location
        img_size = img_loca.size
        x_left = img_location["x"] + 1750
        y_top = img_location["y"] + 620
        x_right = x_left + img_size["width"]
        y_bottom = y_top + img_size["height"] + 20
        img_obj = page_obj.crop((x_left, y_top, x_right, y_bottom))
        pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\SoftwareInstallation\tesseract.exe"
        result_imgToStr = pytesseract.image_to_string(img_obj)
        num_str = re.findall(r"\d",result_imgToStr)
        return "".join(num_str)

