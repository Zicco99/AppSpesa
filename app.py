import requests
from selenium import webdriver
from utils import keys
import time
from datetime import datetime
from threading import Timer
import re
import json


# wait the xpath element appear then execute task (less latency)
def execute_sec(driver, xpath, type, key):
    el = driver.find_elements_by_xpath(xpath)
    while (not el):
        el = driver.find_elements_by_xpath(xpath)
        time.sleep(1)
    if(type == 'input'):
        el[0].send_keys(keys[key])
    if(type == 'click'):
        el[0].click()
    return


def init(driver):
    driver.get("https://www.esselungaacasa.it/ecommerce/nav/auth/supermercato/home.html?streetId=30143801#!/negozio/?header=0")
    execute_sec(driver, '//*[@id="gw_username"]', 'input', 'email')
    execute_sec(driver, '//*[@id="gw_password"]', 'input', 'password')
    time.sleep(3)  # 3 sec to solve captcha manually
    execute_sec(driver, '//*[@id="loginForm"]/div/button', 'click', 'null')
    time.sleep(3)  # 3 sec to load
    scan(driver)

#Scandisce tutti i prodotti presenti sul sito e li salva su un file di testo
def scan(driver):
    array=[]
    i=5000000;
    while(i<6000000):
        driver.get("https://www.esselungaacasa.it/ecommerce/nav/auth/supermercato/home.html#!/negozio/prodotto/{}".format(i))
        time.sleep(2)
        el=driver.find_elements_by_xpath('//*[@id="remodalDialog"]/ng-include/div/p[2]/a')

        if(el): #appare il dialog -> prodotto non esistente
            print("not found")
            el[0].click()

        else: array.append(i) 
        time.sleep(3)
        i+=1
    
    #Fine -> salva sul json tutti i prodotti esistenti
    with open('output.txt', 'w') as filehandle:
        json.dump(array, filehandle)


if __name__ == '__main__':
    driver = webdriver.Chrome('./chromedriver')
    init(driver)
