import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# initialize webdriver
driver = webdriver.Chrome()
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

# reports page
try:
    reports = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="reportsLi"]/a'))
    )
finally:
    reports.click()

# affiliates tab
try:
    affiliates = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="masterAffiliate"]/a'))
    )
finally:
    affiliates.click()

# export csv
remove_overlay = """
function removeElementsByClass(className){
    var elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
};

removeElementsByClass("loading-indicator");
"""

script = 'document.querySelector("#ext-gen447").click();'
# try:
#     export = WebDriverWait(driver, 30).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="ext-gen351"]'))
#     )
# finally:
#     print("exists...")
    # export.execute_script(script)
    # print("Success!")
print("about to remove overlay...")
time.sleep(15)
driver.execute_script(remove_overlay)
print("clicking export...")
time.sleep(15)
driver.execute_script(script)
