import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image

drive=webdriver.Chrome('C:\\users\\moon\\Desktop\\chromedriver.exe')
drive.get('https://naver.com')

drive.save_screenshot('capture.png')
total_width = drive.execute_script("return document.body.offsetWidth")
total_height = drive.execute_script("return document.body.parentNode.scrollHeight")
part = 0
file_name = "part_{0}.png".format(part)
drive.get_screenshot_as_file(file_name)
screenshot = Image.open(file_name)
drive.get_screenshot_as_png()