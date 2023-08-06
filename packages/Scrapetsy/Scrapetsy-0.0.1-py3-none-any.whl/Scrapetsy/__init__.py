'''
This is package to get detail product from www.etsy.com
'''



# Import external package
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import random
import json
import requests
import os
import csv


# Define Class Scrapetsy
class Scrapetsy:

    # define class variable
    def __init__(self,
                 driver_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe',
                 pagination=False,
                 webdriver_opt={'head': '--headless',
                                'sandbox': '--no-sandbox',
                                'gpu': '--disable-gpu',
                                'translate': '--disable-translate'}
                 ):
        self.headers = ['Mozilla/5.0 (Windows NT 6.2; rv:84.0.2) Gecko/20100101 Firefox/84.0.2 anonymized by Abelssoft 298666885',
              'Mozilla/5.0 (Linux; Android 9; POT-LX1A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36',
              'Mozilla/5.0 (Linux; Android 10; SM-J810G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.346',
              'Mozilla/5.0 (Linux; Android 7.0; HM-G552-FL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36',
              'Mozilla/5.0 (Linux; Android 8.0.0; G3221) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 Mobile Safari/537.36',
              'Mozilla/5.0 (Linux; Android 9; COR-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 OPR/61.2.3076.56749',
              'Mozilla/5.0 (Windows; U; Windows NT 5.0; fr-FR; rv:1.7.7) Gecko/20050414 Firefox/50.0.1',
              'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 OcIdWebView ({\x22os\x22:\x22iOS\x22,\x22appVersion\x22:\x225.58.3\x22,\x22app\x22:\x22com.google.Maps\x22,\x22osVersion\x22:\x2214.2\x22,\x22style\x22:2,\x22isDarkTheme\x22:false,\x22libraryVersion\x22:\x221.19.10.0\x22,\x22zoom\x22:0.90947546531302881})',
              'Mozilla/5.0 (Linux; Android 6.0.1; Moto G Play Build/MPI24.241-15.3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/290.0.0.44.121']
        self.driver_path = driver_path
        self.pagination = pagination
        self.webdriver_opt = webdriver_opt

    # define class function
    def get_url(self, url, proxies):
        print('getting urls...')
        if self.pagination is False:
            user_agent=random.Random(500).choice(self.headers)
            proxies = random.Random(500).choice(proxies)
            proxies = f"{proxies['ip']}:{proxies['port']}"
            options = Options()
            options.add_argument(self.webdriver_opt['head'])
            options.add_argument(self.webdriver_opt['sandbox'])
            options.add_argument(self.webdriver_opt['gpu'])
            options.add_argument(self.webdriver_opt['translate'])
            options.add_argument(f"user-agent={user_agent}")
            options.add_argument('--proxy-server=%s' % proxies)
            driver = webdriver.Firefox(executable_path=self.driver_path, options=options)
            driver.get(url)
            response = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, 'content')))
            parent = response.find_element(By.CSS_SELECTOR, ".wt-grid.wt-grid--block.wt-pl-xs-0")
            child = parent.find_elements(By.CSS_SELECTOR,".wt-list-unstyled")
            hasil=[]
            for i in child:
                try:
                    item=i.find_element(By.TAG_NAME, "a").get_attribute('href')
                    print(f'{item} collected')
                    hasil.append(item)
                except StaleElementReferenceException:
                    pass
            driver.quit()
            print(f'{len(hasil)} urls collected')
        else:
            parsed_url = url.rsplit(sep='page=', maxsplit=1)
            page = int(parsed_url[1])
            url_wo_page = parsed_url[0]
            hasil = []
            while 1:
                pag_url = f'{url_wo_page}page={str(page)}'
                print(pag_url)
                # try:
                user_agent = random.Random(500).choice(self.headers)
                prox = random.Random(500).choice(proxies)
                prox = f"{prox['ip']}:{prox['port']}"
                options = Options()
                options.add_argument(self.webdriver_opt['head'])
                options.add_argument(self.webdriver_opt['sandbox'])
                options.add_argument(self.webdriver_opt['gpu'])
                options.add_argument(self.webdriver_opt['translate'])
                options.add_argument(f"user-agent={user_agent}")
                options.add_argument('--proxy-server=%s' % prox)
                driver = webdriver.Firefox(executable_path=self.driver_path, options=options)
                driver.get(pag_url)
                response = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.ID, 'content')))
                try:
                    parent = response.find_element(By.CSS_SELECTOR, ".wt-grid.wt-grid--block.wt-pl-xs-0")
                    child = parent.find_elements(By.CSS_SELECTOR, ".wt-list-unstyled")
                    for i in child:
                        try:
                            item = i.find_element(By.TAG_NAME, "a").get_attribute('href')
                            print(f'{item} collected')
                            hasil.append(item)
                        except StaleElementReferenceException:
                            pass
                    print(f'page {str(page)} collected')
                    page += 1

                    driver.quit()
                except NoSuchElementException:
                    driver.quit()
                    break
            print(f'{len(hasil)} urls collected')
        return hasil

    def get_proxy(self, url='https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc'):
        print('getting proxy...')
        try:
            # Request keys and values from Geonode
            proxy_json_url = json.loads(requests.get(
                url=url).text)

            # Return random proxy
            return proxy_json_url['data']
        except requests.exceptions.ProxyError:
            ### Return '' string on error
            return ""


    def get_detail(self, url, proxies):
        print('getting details...')
        # initial variable
        data = {'image': '', 'title': '', 'price': '', 'outlet_name': '', 'link_outlet': '', 'item_sold': '',
                'detail': [], 'description': '', 'reviews': '', 'url': ''}

        user_agent = random.Random(500).choice(self.headers)
        prox = random.Random(500).choice(proxies)
        prox = f"{prox['ip']}:{prox['port']}"
        options = Options()
        options.add_argument(self.webdriver_opt['head'])
        options.add_argument(self.webdriver_opt['sandbox'])
        options.add_argument(self.webdriver_opt['gpu'])
        options.add_argument(self.webdriver_opt['translate'])
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument('--proxy-server=%s' % prox)
        driver = webdriver.Firefox(executable_path=self.driver_path, options=options)
        driver.get(url)
        response = WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'div.body-wrap')))
        data['image'] = response.find_element(By.CSS_SELECTOR, 'li.carousel-pane:nth-child(1) > img:nth-child(1)').get_attribute('src')
        data['title'] = response.find_element(By.CSS_SELECTOR, 'h1.wt-text-body-03').text

        # get price
        prices1 = response.find_element(By.CSS_SELECTOR, "p.wt-text-title-03.wt-mr-xs-1")
        prices2 = prices1.find_elements(By.TAG_NAME, 'span')
        try:
            data['price'] = prices2[-1].text
        except IndexError:
            data['price'] = prices1.text

        data['outlet_name'] = response.find_element(By.CSS_SELECTOR, 'p.wt-text-body-01.wt-mr-xs-1 > a > span').text
        data['link_outlet'] = response.find_element(By.CSS_SELECTOR, 'p.wt-text-body-01.wt-mr-xs-1 > a').get_attribute('href')

        try:
            data['item_sold'] = response.find_element(By.CSS_SELECTOR, 'div.wt-display-inline-flex-xs.wt-align-items-center.wt-flex-wrap > span.wt-text-caption').text
        except NoSuchElementException:
            data['item_sold'] = '0'

        # get detail
        details = response.find_elements(By.CSS_SELECTOR, 'ul.wt-text-body-01 > li')
        detail_list = []
        for j in details:
            detail_list.append(j.text)
        data['detail'] = detail_list

        data['description'] = response.find_element(By.CSS_SELECTOR, 'p.wt-break-word').text
        data['reviews'] = response.find_element(By.CSS_SELECTOR, 'h2.wt-mr-xs-2').text
        data['url'] = url

        print(f'{url} collected')

        driver.quit()
        return data

    def create_file(self, data, filepath='/result/result.json'):
        print('Creating file...')
        ext = filepath.split(".")[-1]
        folder = filepath.rsplit("/", 1)[0]
        if ext == 'json':
            try:
                os.mkdir(folder)
            except FileExistsError:
                pass
            with open(filepath, 'w+', encoding="utf-8", newline='') as f:
                json.dump(data, f)
                f.close()

        elif ext == 'csv':
            try:
                os.mkdir(folder)
            except FileExistsError:
                pass
            with open(filepath, 'w+', encoding="utf-8", newline='') as f:
                headers = ['image', 'title', 'price', 'outlet_name', 'link_outlet', 'item_sold', 'detail',
                           'description', 'reviews', 'url']
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for i in data:
                    writer.writerow(i)
                f.close()

        else:
            print('Unknown format file')
        print(f'{filepath} created')

if __name__ == '__main__':
    se = Scrapetsy(driver_path='C:/geckodriver-v0.31.0-win64/geckodriver.exe',
                                pagination=True)
    proxies = se.get_proxy()
    urls = se.get_url(url='https://www.etsy.com/search?q=gift+for+women&ref=pagination&anchor_listing_id=737271222&page=250', proxies=proxies)
    data = []
    for url in urls:
        data.append(se.get_detail(url, proxies = proxies))
    print(f'{len(data)} collected')
    se.create_file(data=data, filepath='C:/project/Scrapetsy/result/result.csv')