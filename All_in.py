import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium.webdriver.common.by import By


class Searcher:
    def __init__(self):
        self.respond = requests.get(
            "https://fly.pl/oferta/wakacje/wakacje-all-inclusive/oferta/p:3/?filter[dest]=15:,39:,44:,3269"
            ":,2:,5:,8:&filter[hotelids]=0&filter[cityids]=0&filter[cregids]=&filter[ofrType]=&filter[addObj"
            "Type]=&filter[whenFrom]=06-06-2022&filter[whenTo]=30-10-2022&filter[duration]=6:8&filter[from]"
            "=Gdańsk&filter[person]=2&filter[child]=0&filter[price]=0&filter[PriceFrom]=0&filter[PriceTo]="
            "30000&filter[addCategory]=10&filter[addCatering]=1&filter[addMisc]=0&filter[addTransport]=F&"
            "filter[fp]=1&order_by=ofr_price&filter[tourOperator]=0")
        self.web_site = self.respond.text
        self.soup = BeautifulSoup(self.web_site, "html.parser")

        self.chrome_driver_path = "C:/Users/agnie/Developer/chromedriver.exe"
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path, options=self.options)
        self.driver.get(
            "https://docs.google.com/forms/d/e/1FAIpQLSeqiJ2BO-CeT2nZHlVQFnvtvCi8euF_d8tyTlhq5y5rPmngVw/viewform?usp="
            "sf_link")

        self.all_data = []

        self.list_offers = self.soup.find_all(class_="card-offer-search price-pos")

    def list_of_parts(self):
        for i in self.list_offers:
            temp_list = []
            link = i.attrs["data-phref"]
            price = int(re.findall("[0-9]{1} [0-9]{3}", str(i.getText()))[0].replace(" ", ""))
            where = link.split("/")[4].replace(',', " ")
            try:
                mark = re.findall("^.*opinii", str(i.getText()), re.MULTILINE)[0]
            except:
                mark = "None"
            when = re.findall("[0-9]{2}\.[0-9]{2}\.[0-9]{4}", str(i.getText()))[0]

            temp_list.append(link)
            temp_list.append(price)
            temp_list.append(where)
            temp_list.append(mark)
            temp_list.append(when)
            self.all_data.append(temp_list)

    def fill_forms(self):
        for i in self.all_data:
            self.driver.implicitly_wait(5)
            self.driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(i[0])

            self.driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/'
                                'input').send_keys(i[1])

            self.driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/'
                                'input').send_keys(i[2])

            self.driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/'
                               'input').send_keys(i[3])

            self.driver.find_element(By.XPATH,
                              '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/'
                              'input').send_keys(i[4])

            self.driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()

            self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()

    def quit_form(self):
        self.driver.quit()
