import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver import ActionChains

import pyautogui

pyautogui.PAUSE = 0.5

class simc():
    chromedriver = "/Users/heweiwen/Downloads/work/Solf/chrome-mac/chromedriver"
    def __init__(self):
        chromedriver = "/Users/heweiwen/Downloads/work/Solf/chrome-mac/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chromedriver)
        self.driver.maximize_window()
        home_url = 'http://www.taobao.com'
        self.driver.get(home_url)
        self.driver.implicitly_wait(5)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        })
        self.action_chains = ActionChains(self.driver)

        # self.browser = webdriver.Chrome(r'/Users/heweiwen/Downloads/work/Solf/chrome-mac/chromedriver')
        # self.browser.maximize_window()
        # self.domain = 'http://www.taobao.com'
        # self.browser.implicitly_wait(5)
        # self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""",
        # })
        # self.action_chains = ActionChains(self.browser)

    def login(self, username, password):
        self.browser.get(self.domain)
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]').click()
        self.browser.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
        self.browser.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)
        time.sleep(1)
        coords = pyautogui.locateOnScreen("login.png", confidence=0.5)
        x, y = pyautogui.center(coords)
        time.sleep(2)
        pyautogui.leftClick(x, y)

    def get_nickname(self):
        try:
            print(self.browser.find_element_by_class_name('site-nav-user').text)
        except NoSuchElementException:
            return '未获取到用户名'

if __name__ == '__main__':
    simc = simc()
    simc.login('heweiwen610738891', 'He19891025')
    simc.get_nickname()