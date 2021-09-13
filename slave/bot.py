from selenium import webdriver


IP = ""
PORT = ""
PROXY = IP + ":" + PORT
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome = webdriver.Chrome("./chromedriver", chrome_options=chrome_options)

chrome.get("https://www.google.com/search?channel=fs&client=ubuntu&q=what+is+my+ip+address")
