# coding: utf-8
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    driver.get('http://www.google.com.br')
    
    try:
	box = driver.wait.until(EC.presence_of_element_located((By.NAME, 'q')))
	box.send_keys(query)
	button = driver.wait.until(EC.element_to_be_clickable((By.NAME, 'btnG')))
	#box.send_keys(query)
	button.click()
    
    except TimeoutException: 
	print('Box or Button not found in gloogle.com')
