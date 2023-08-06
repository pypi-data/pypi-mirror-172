from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import requests
import enum
from slugify import slugify


class ERRORS(enum.IntEnum):
    """
    Contains constant errors for Scrapis
    """
    SUCCESS = 0
    ERROR_FETCHING_DOWNLOAD = 15
    NO_DOWNLOAD_LINK_FOUND = 6
    KEYRING_NOT_INSTALLED = 10
    CANNOT_LOGIN_GPLAY = 15


class Apkcombo():
    """docstring for ."""

    def __init__(self, args=None):
        self.driver_path = "/usr/bin/chromedriver"
        self.download_folder = "/home/4apis.com"
        self.binary_location = None
        if args.dpath is not None:
            self.driver_path = args.dpath
        if args.folder is not None:
            self.download_folder = args.folder[0]
        capabilities = DesiredCapabilities.CHROME
        capabilities["pageLoadStrategy"] = "normal"
        proxy = "203.13.32.211:80"
        # configure chrome browser to not load images and javascript
        options = webdriver.ChromeOptions()
        #if args.bl is not None:
            #options.binary_location = args.bl
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # set window size to native GUI size
        options.add_argument("--window-size=1920,1080")
        options.add_argument("start-maximized")  # ensure window is full-screen
        options.add_argument('disable-infobars')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        # options.add_argument('--proxy-server=%s' % proxy)
        options.add_experimental_option(
            # this will disable image loading
            "prefs", {"useAutomationExtension": False,
                      "intl.accept_languages": "en,en_US"}
        )
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Remote(command_executor="http://161.97.144.140:4444", options=options, desired_capabilities=capabilities)
        self.version = None
        self.filename = None

    def getDownloadLink(self, appID=None):
        self.driver.get("https://apkcombo.com/search")
        # wait for page to load
        button = WebDriverWait(driver=self.driver, timeout=30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.button-search.is-link')))
        # First check if privacy dialog exists
        # print(WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'qc-cmp2-ui'))))
        try:
           acceptBtn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[mode="primary"]')))
           if(acceptBtn):
              acceptBtn.click()
        except:
           pass
        #print("Search input showing")
        input = self.driver.find_element(By.NAME, "q")
        input.send_keys(appID)
        button.click()
        # sumbitBtn = self.driver.find_element(By.ID, 'apksumbit')
        #print("submitting button")
        # Sumbit button
        # self.driver.execute_script("arguments[0].scrollIntoView();", sumbitBtn)
        # driver.execute_script("arguments[0].click();", sumbitBtn)
        # wait for URL to change with 15 seconds timeout

        downloadPage = WebDriverWait(driver=self.driver, timeout=20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.button.is-success'))
        )
        data = {}
        self.version = self.driver.find_element(
            By.CSS_SELECTOR, '.app_header .info .version').text
        self.version = slugify(self.version, max_length=20,
                               word_boundary=True, separator=".")
        self.filename = '{filename}.{version}{extension}'.format(
            filename=appID, version=self.version, extension='.apk')
        self.filename = slugify(
            self.filename, max_length=200, word_boundary=True, separator=".")
        downloadPage.click()
        dlink = WebDriverWait(driver=self.driver, timeout=20).until(
            EC.presence_of_element_located((By.ID, 'best-variant-tab'))
        )
        #print(linksTab)
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, '.file-list li a')
        links = [elem.get_attribute('href') for elem in elements]
        #print("Link has been fetched {link}".format(link = links[0]))
        # Download file
        # time.sleep(15)
        filterApks = []
        for link in links:
            if (".apk" in link and "&ip=" in link):
                filterApks.append(link)
        dlink = None
        #print(json.dumps(filterApks))
        try:
            dlink = filterApks[0]
        except IndexError:
            raise ERRORS.NO_DOWNLOAD_LINK_FOUND
        data['version'] = self.version
        data['filename'] = self.filename
        data['link'] = dlink
        self.driver.close()
        return data

    def download(self, appID):
        data = {"ok": False, "code": 200, "filename": None, "message": None}
        try:
            link = self.getDownloadLink(appID)["link"]
            r = requests.get(link, allow_redirects=True)
            # Check if download folder exists or create it
            if not os.path.isdir(self.download_folder):
                os.makedirs(self.download_folder, exist_ok=True)
            filepath = os.path.join(self.download_folder, self.filename)
            if os.path.isfile(filepath):
                data["message"] = "File {filename} already exists, skipping.".format(
                    filename=self.filename)
            else:
                open(filepath, 'wb').write(r.content)
                data["message"] = "File has been downloaded successfully {filename}".format(
                    filename=self.filename)
            data["ok"] = True
            data["filename"] = self.filename
        except Exception as e:
            data["message"] = "Failed to download file {filename}".format(
                filename=self.filename)
            data["code"] = 500
        return data
