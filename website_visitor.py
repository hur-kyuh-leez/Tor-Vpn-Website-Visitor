from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
import os
import time
import signal
import sys
import random



class Visitor():
    def __init__(self,driver_type='firefox'):
        self.driver_type = driver_type
        pass
    def set_driver(self):
        os.system('tor&')
        if self.driver_type == 'firefox':
            firefox_driver = '/usr/bin/geckodriver' # change this to your geckodriver directory
            profile = webdriver.FirefoxProfile()
            profile.set_preference("media.volume_scale", "0.0")
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.socks", "127.0.0.1")
            profile.set_preference("network.proxy.socks_port", 9050) # Port Opened by Tor
            profile.update_preferences()
            options = Options()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options, executable_path=firefox_driver)
        elif self.driver_type == 'chrome':
            chrome_driver = '/usr/bin/chromedriver' # change this to your chromedriver directory
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--mute-audio")
            time.sleep(4)
            options.add_argument('--proxy-server=socks5://localhost:9050')

            self.driver = webdriver.Chrome(chrome_options=options,
                                            executable_path=chrome_driver)

    def get_page_source(self, url):
        self.driver.get(url)
        print("========================================================================================================")
        print(self.driver.page_source)
        time.sleep(1)

    def go_to_targeted_url(self, url):
        self.driver.get(url)
        print('visiting:', url)
        time.sleep(random.randint(2, 8))

    def close_tor(self):
        os.system("pkill tor")
        time.sleep(1)

    def close_driver(self):
        pid = self.driver.service.process.pid
        print(pid)
        self.driver.quit()
        try:
            os.kill(int(pid), signal.SIGTERM)
            os.sys('pkill chromedrive')
            os.sys('pkill chromium-browse')
            print(
                "========================================================================================================")
            print("Killed selinum.driver using processID")
        except ProcessLookupError as ex:
            pass



if __name__ == "__main__":

    links = [
        'URL_1',
        'URL_2',
                     ]

    def maincode(num): # how many times do you want to visit your website?
        for i in range(num):
            for link in links:
                try:
                    visitor = Visitor('chrome')
                    visitor.set_driver()
                    visitor.get_page_source('http://icanhazip.com/')  # get ip
                    visitor.go_to_targeted_url(link)
                    visitor.close_tor()
                    visitor.close_driver()

                except Exception as e:
                    visitor.close_tor()
                    visitor.close_driver()
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(
                        "========================================================================================================")
                    print(exc_type, fname, exc_tb.tb_lineno)

    # Example visit 20 times
    maincode(20)



