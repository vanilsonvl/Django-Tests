#coding: utf-8
from django.core.management.base import BaseCommand
import time
from selenium import webdriver
from dt_selenium.utils import init_driver, lookup

class Command(BaseCommand):
    help = 'Selenium Tests'

    def handle(self, *args, **kwargs):
        driver = init_driver()
        lookup(driver, 'Python')
	time.sleep(5)
	driver.quit()
