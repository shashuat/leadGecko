import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from .models import Leadlist ,List
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
import sqlite3

service = ChromeService(executable_path=ChromeDriverManager().install())
mobile_emulation = {

    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }


option = Options()

# option.add_argument('--headless')

# Pass the argument 1 to allow and 2 to block
# option.add_experimental_option("prefs", { 
#     "profile.default_content_setting_values.notifications": 1
# })

# START_URL = "https://www.justdial.com/Delhi/Gift-Shops/nct-10231352/page-1"

 #input('Past Your Link here and press ENTER? \n')

class CatalogsScrapper:
    def __init__(self, browser, filename, count, dataId):

        if not isinstance(browser, webdriver.Chrome):
            raise TypeError("browser must be a instance of webdriver.Chrome")

        if os.path.exists(filename):
            os.remove(filename)
        self.dataId = dataId
        self.filename = filename
        self.browser = browser
        self.links = []
        self.comp = False
        self.count = count
        self.conn = sqlite3.connect('db.sqlite3')
        self.cursor = self.conn.cursor()
        self.createTable()

    def createTable(self):
        command = f'''CREATE TABLE IF NOT EXISTS {str(self.dataId)} (
         title VARCHAR(100) NOT NULL,
         rating VARCHAR(10) NOT NULL,
         address VARCHAR(250) NOT NULL,
         phoneno VARCHAR(20) NOT NULL,
         link VARCHAR(2050) );'''
        self.cursor.execute(command)

    # scrapping data from link one by one
    def scrappDataFromLink(self):
        if os.path.exists(self.filename):
            f = open(self.filename, "r")
            self.browser.get('https://www.justdial.com/')
            for x in f:
                chrome_options = Options()
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")

                driver = webdriver.Chrome(options = chrome_options, service=service)
                print('opening Link....')
                print(x)
                driver.get(x)
                time.sleep(10)

                try:
                    Title = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div[3]/div/div[1]/span')
                    title = Title.text
                except NoSuchElementException:
                    try:
                        Title = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div[2]/span/a/span/div/div/div[1]/div[1]')
                        title = Title.text
                    except NoSuchElementException:
                        print('Unable to fetch title')
                        title = ''
                try:
                    Rating = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div[3]/div/div[2]/div[1]')
                    rating = Rating.text[:-1]
                except NoSuchElementException:
                    try:
                        Rating = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div[2]/span/a/span/div/div/div[1]/div[3]/span[1]/span[1]')
                        rating = Rating.text[:-1]
                    except NoSuchElementException:
                        print('Unable to fetch rating')
                        rating = ''

                try:
                    Address = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div[10]/span/span[2]')
                    address = Address.text[:-13]
                except NoSuchElementException:
                    try:
                        Address = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div[3]/div[2]/span/span/div/div[2]/div/div[6]/span/span[1]/span[2]')
                        address = Address.text
                    except NoSuchElementException:
                        try:
                            Address = driver.find_element(by=By.XPATH, value='/html/body/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div[2]/div/div[1]/div/div[3]/div[2]/span/span/div/div[2]/div/div[5]/span/span[1]/span[2]')
                            address = Address.text[:-13]
                        except NoSuchElementException:
                            print('Unable to fetch address')
                            address = ''
                try:
                    number = driver.find_elements(by=By.CLASS_NAME, value='dpvstephnum')
                    numArray = []
                    for num in number:
                        numArray.append(num.text) 
                        # print (num.text)
                        # phone = Phone.text
                except:
                    numArray = []
                    print('phone number is not defined')

                if len(numArray) == 0:
                    numArray.append("")

                Obj = {
                    "title": title,
                    "rating": rating,
                    "address": address,
                    "phone": numArray
                }

                print(Obj)
                command = f"INSERT INTO {str(self.dataId)} (title,rating,address,phoneno,link) VALUES ('{title}', '{rating}', '{address}', '{str(numArray[0])}', '{x}');"
                self.cursor.execute(command)
                self.conn.commit()
                driver.quit()
                #data=Leadlist(listname="Grocery store delhi L2",name=title,list_owner="sagar",address=address,reviews=rating,phone=numArray)
                #data.save()



    def getArrayLinksAndScrapData(self):
        if os.path.exists(self.filename):
            num_lines = sum(1 for line in open('links.txt'))
            print(num_lines)
            if num_lines >= self.count:
                print('links almost done now it getting data from link')
                self.scrappDataFromLink()


    def storeLink(self):
        # open file with mode a
        f = open(self.filename, "a")
        # Looping on each catalog links on per page
        for Link in self.links:
            f.write(Link + '\r')
        f.close()
        self.getArrayLinksAndScrapData()

    def getNextPageLink(self, currentUrl):
        link = currentUrl.split('-')
        num = link[-1]
        num = int(num)
        num = num + 1
        num = str(num)
        link[-1] = num
        newUrl = '-'.join(link)
        return newUrl

    def scrape_justdial_Link(self):
        elems = self.browser.find_elements(by=By.CSS_SELECTOR, value='.cntanr')
        
        if len(elems) == 0:
            self.comp = True
            print('done')
            return 
        
        for elem in elems:
            # print (elem.get_attribute('data-href'))
            self.links.append(elem.get_attribute('data-href'))
        print('done')
        return
    
    def scrap_links(self, pageUrl, option, service):
        next_page_link = pageUrl
        print('Scrapping all links URL')
        print()
        while True:
            try:
                print('Scrapping, ', next_page_link)
                self.browser.get(next_page_link)
                self.scrape_justdial_Link()
                if self.comp:
                    print('All links scrapped')
                    break
                self.browser.quit()
                next_page_link = self.getNextPageLink(next_page_link)
                self.browser = webdriver.Chrome(options = option, service=service)
            except InvalidArgumentException as error:
                print('All links scrapped')
                break
        return
        

    def getLinksData(self, pageUrl, option, service):
        try:
            self.scrap_links(pageUrl, option, service)
            print('Got links\nScraping data')
            self.storeLink()
            print('Data Scraping done\nSaving data')
            self.conn.commit()
            self.conn.close()
            return 1
        except:
            return 0

        

def main():
    START_URL = 'https://www.justdial.com/Delhi/Gift-Shops/nct-10231352/page-1'
    count = (int(input('Please Enter how much data do you want to scrape? Example: 10, 20, 30, 40.....more \n')))
    browser = webdriver.Chrome(options=option, service=service)
    catalogs_scrapper = CatalogsScrapper(browser=browser, filename='links.txt', count=count, dataId='authenticate_leadlist')
    error = catalogs_scrapper.getLinksData(pageUrl=START_URL, option=option, service=service)
    print(error)


if __name__ == "__main__":
    main()
