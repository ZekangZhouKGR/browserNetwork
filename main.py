from browsermobproxy import Server,RemoteServer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import json
import time

blacklist = []


class RequestLog(object):
    def __init__(self, har_name, blacklist = [], har_options = {'captureHeaders':True,'captureContent':True }):
        import os
        host = ''
        assert host != ''
        port = 8080
        proxy_port = '24342'
        self.server = RemoteServer(host=host,port=port)
        self.proxy = self.server.create_proxy()
        self.proxy.new_har(har_name,options = har_options)
        for host,code in blacklist:
            self.setBlackList(host, code)

    def setBlackList(self, host, code):
        self.proxy.blacklist(host,code)

    def setOptions(self, options):
        options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))

    def getHar(self):
        return self.proxy.har

    def getEntries(self):
        return self.proxy.har['log']['entries']

    def close(self):
        try:
            if self.server != None:
                self.server.stop()
        except:
            pass
        if self.proxy != None:
            self.proxy.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def add_cookies(bowser):
    import json
    home_page = ''
    assert home_page != ''
    bowser.get(home_page)
    cookies_file = 'cookies.json' 
    if os.path.isfile(cookies_file):
        with open(cookies_file,'r') as f:
            cookies = json.load(f)
        for cookie in cookies:
            bowser.add_cookie({
                'domain':cookie['domain'],
                'name':cookie['name'],
                'value':cookie['value']
                })
        bowser.get(home_page)
        return True
    return False


def main():
    chrome = None;
    requestlog = None;
    try:
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1280,720')

        driver_path = os.environ['CHROMEDRIVER'] if 'CHROMEDRIVER' in os.environ else 'D:/chromedriver/chromedriver.exe'

        requestlog = RequestLog('rlog.log',blacklist = blacklist)
        requestlog.setOptions(chrome_options)
        chrome = webdriver.Chrome(executable_path=driver_path,options = chrome_options)
        add_cookies(chrome)
        # 此处可以添加自动化方法
        input()
    finally:
        if chrome != None:
            chrome.get_screenshot_as_file("error.png")
            chrome.quit()
        if requestlog != None:
            har = requestlog.getHar()
            har['log']['entries'] = [*filter(lambda x: 'attach.php' in x['request']['url'],har['log']['entries'])]
            json.dump(har,open('rlog_' + str(int(time.time())) + '.har','w'))
            requestlog.close();

if __name__ == '__main__':
    main()

    