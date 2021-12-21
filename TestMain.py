# import os
import time
import re

import pytest
import yaml
from PIL import Image
import pytesseract
from selenium.webdriver.support.wait import WebDriverWait

# #java -jar /d/Software/Selenium/SoftwareDownload/seleniumGrid_3.141.59/selenium-server-standalone-3.141.59.jar -role hub -maxSession 10
# #java -jar /d/Software/Selenium/SoftwareDownload/seleniumGrid_3.141.59/selenium-server-standalone-3.141.59.jar -role node -port 5555 -hub http://192.168.199.1:4444/grid/register -maxSession 5 -browser browserName=chrome,seleniumProtocol=WebDriver,maxInstances=5
#
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
#
from selenium.webdriver.common.by import By


import stat
import os

# os.chmod(r"D:\Software\Tesseract-OCR\SoftwareInstallation",stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH|stat.S_IXUSR|stat.S_IRUSR|stat.S_IWUSR|stat.S_IWGRP|stat.S_IXGRP)
# os.remove(r"D:\Software\Tesseract-OCR\SoftwareInstallation")
#
# # try {
# # driver = WebDriver(new URL("http://192.168.0.245:4444/wd/hub"), capability);
# #
# # driver.get("http://www.baidu.com");
# #
# # driver.quit();
# #
# # } catch (MalformedURLException e) {
# #   e.printStackTrace();
# #
# # }
import logging
'''
    测试特定功能验证使用  
'''
class Test():
    def getCAPTCHA(self):
        driver = get_driver()
        time.sleep(1)
        driver.save_screenshot("./Pictures/CAPTCHA.png")
        page_obj = Image.open("./Pictures/CAPTCHA.png")
        img_loca = driver.find_element(By.XPATH, "//*[@id='pane-first']/form/div[4]/div/span[2]/img")
        time.sleep(1)
        location = img_loca.location
        # print(location)
        size = img_loca.size
        # print(size)
        x_left = location["x"]
        y_top = location["y"]
        x_right = x_left + size["width"]
        y_bottom = y_top + size["height"]
        img_obj = page_obj.crop((x_left, y_top, x_right, y_bottom))
        img_obj.show()
        # pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Pycharm\DocumentsDownload\Projects\SaaSCyberWaterSupplyGWAuto\Tesseract-OCR\tesseract.exe"
        pytesseract.pytesseract.tesseract_cmd = r"D:\Software\Tesseract-OCR\SoftwareInstallation\tesseract.exe"
        result_imgToStr = pytesseract.image_to_string(img_obj)
        a = re.findall(r"\d", result_imgToStr)
        print("".join(a))

def get_driver():
    caps = {}
    caps["browserName"] = "chrome"
    # #caps["browserName"] = os.getenv('browserName',None)
    caps["platform"] = "WINDOWS"
    caps["javascriptEnabled"] = True
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)

    return driver

# @pytest.mark.parametrize(("a,b,c,d"),yaml.safe_load(open("./Data/login.yaml",encoding='utf-8'))["loginDatasValues"])
#     #@pytest.mark.parametrize(("a,b,c"),[[1,2,3],[2,3,4]])
# def test_a(a,b,c,d):
#     print(a,b,c,d)
#     print("test")

if __name__ == "__main__":

    # 获取当前时间
    print(time.localtime(time.time()+172800))
    print(time.strftime("%H:%M:%S %m-%d-%Y", time.localtime(time.time() + 172800)))
    driver = get_driver()
    driver.maximize_window()
    driver.get("https://www.baidu.com")
    text = driver.find_element(By.XPATH,'//*[@id="hotsearch-content-wrapper"]/li[3]/a/span[2]')
    driver.quit()




