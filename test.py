import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture()
def driver():

    mobile_emulation = {
        "deviceMetrics": { "width": 624, "height": 1078, "pixelRatio": 3.0 },
        "userAgent": "Chrome/18.0.1025.166 Mobile Safari/535.19"
    }

    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    yield driver
    if driver:
        driver.quit()

def test_make_screenshot(driver):

    wait = WebDriverWait(driver, 10)

# open the page
    driver.get('https://m.twitch.tv')
    driver.find_element(By.XPATH, '//*[@aria-label="Search"]').click()

# search for StarCraft II
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@placeholder="Search..."]')))
    driver.find_element(By.XPATH, '//*[@placeholder="Search..."]').send_keys('StarCraft II')
    driver.find_element(By.XPATH, '//*[@placeholder="Search..."]').send_keys(Keys.RETURN)
    driver.find_element(By.XPATH, '//*[@placeholder="Search..."]').send_keys(Keys.PAGE_DOWN)
    driver.find_element(By.XPATH, '//*[@placeholder="Search..."]').send_keys(Keys.PAGE_DOWN)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//h2')))
    driver.find_elements(By.XPATH, '//h2')[2].click()

# close pop-up
    if len(driver.find_elements(By.XPATH, '//*[@id="PopUp"]')) > 0:
        driver.find_element(By.XPATH, '//*[@id="close"]').click()

# wait until the video is loaded
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-a-target="player-play-pause-button"]')))

# make a screenshot
    driver.save_screenshot('screenshot.png')
