import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

# set options
# opts = Options()
# opts.set_headless()

# path to save csv file
path = '/Users/pbegle/Selenium/Downloads'

# To prevent download dialog
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', path)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

# initialize webdriver
# driver = webdriver.Firefox(options=opts)
driver = webdriver.Firefox(firefox_profile=profile)
driver.get("https://login.vervedirect.com/")

# username
username = driver.find_element_by_id("u")
username.clear()
username.send_keys(os.environ['VERVE_USERNAME'])

# password
password = driver.find_element_by_id("password")
password.clear()
password.send_keys(os.environ['VERVE_PASSWORD'])

# login
submit = driver.find_element_by_id("submitButton")
submit.click()
print("login successful")

# reports page
try:
    reports = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/ul/li[3]/a'))
    )
finally:
    reports.click()
print("moved to reports page...")

# affiliates tab
try:
    affiliates = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/ul/li[3]/div/div/div/div/div/div[2]/div/ul/li[1]/a'))
    )
finally:
    affiliates.click()
print("clicked affiliates tab...")

# export csv
# remove overlay blocking export button
remove_overlay = """
                    function removeElementsByClass(className){
                        var elements = document.getElementsByClassName(className);
                        while(elements.length > 0){
                            elements[0].parentNode.removeChild(elements[0]);
                        }
                    };

                    removeElementsByClass("loading-indicator");
                 """

# get array of buttons and click the last one; export button
script = 'document.querySelectorAll(".x-toolbar-right-ct button")[5].click()'

time.sleep(3)
print("removing overlay...")
driver.execute_script(remove_overlay)

time.sleep(3)
print("downloading csv...")
driver.execute_script(script)
print("success!")