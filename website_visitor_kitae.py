# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
import os
import time
import signal
import sys
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pexpect
import getpass
from PRIVATE_INFO import sudo_password
import re


# Utils
def sudo_command(command, sudo_password):
    username = getpass.getuser()
    child = pexpect.spawn(f'sudo {command}')
    child.expect_exact(f'[sudo] password for {username}:')
    child.sendline(sudo_password)
    child.expect(pexpect.EOF, timeout=None)


def get_blogs_list(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    links = soup.findAll('a')
    href_list = []
    for link in links:
        href = link.attrs['href']
        if '/PostView' in href:
            href = str(f'https://blog.naver.com/{href}')
            href_list.append(href)
    return href_list


class Visitor():
    def __init__(self,driver_type='firefox'):
        self.driver_type = driver_type
        pass
    def set_driver(self):
        os.system('tor&')
        if self.driver_type == 'firefox':
            firefox_driver = '/usr/bin/geckodriver'
            profile = webdriver.FirefoxProfile()
            profile.set_preference("media.volume_scale", "0.0")
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.socks", "127.0.0.1")
            profile.set_preference("network.proxy.socks_port", 9050) # 토르 연 포트
            profile.update_preferences()
            options = Options()
            options.add_argument("--headless")
            self.driver = webdriver.Firefox(firefox_profile=profile, firefox_options=options, executable_path=firefox_driver)
        elif self.driver_type == 'chrome':
            chrome_driver = '/usr/bin/chromedriver'
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
        # os.system("pkill tor")
        sudo_command('pkill tor', sudo_password)
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


    def maincode(num, url):
        for i in range(num):  # 조회수 늘리고 싶은 만큼
            blogId = re.search('blogId=(.*?)&', url).group(1)
            print(str(blogId))
            links = get_blogs_list(url)
            link = random.choice(links)
            try:
                visitor = Visitor('chrome')
                visitor.set_driver()
                visitor.get_page_source(f'http://blog.naver.com/NVisitorgp4Ajax.nhn?blogId={blogId}')  # get 조회수
                visitor.get_page_source('http://icanhazip.com/')  # get ip
                visitor.go_to_targeted_url(link)
                visitor.close_tor()
                visitor.close_driver()
                # if visitor.driver_type == 'firefox':
                #     os.sys('pkill firefox')
                # elif visitor.driver_type == 'chrome':
                #     os.sys('killall "Google Chrome"')
                # time.sleep(1)
            except Exception as e:
                visitor.close_tor()
                visitor.close_driver()
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(
                    "========================================================================================================")
                print(exc_type, fname, exc_tb.tb_lineno)


    maincode(999999, YOUR_URL)



