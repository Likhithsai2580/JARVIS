from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import colorama
from colorama import Fore, Style
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
from functools import lru_cache

# Disable Selenium logging to reduce noise
LOGGER.setLevel(logging.ERROR)

# Initialize Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.headless = True

# Initialize WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)
website = "https://ttsmp3.com/text-to-speech/British2English/"
driver.get(website)

# Set implicit wait for the driver
driver.implicitly_wait(10)

# Wait for the dropdown to be clickable
select_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'sprachwahl')))

# Select 'British English / Brian' from the dropdown
Buttonselection = Select(select_element)
Buttonselection.select_by_visible_text("British English / Brian")

# Cache the 'speak' function
@lru_cache(maxsize=128)  # Adjust maxsize according to your memory constraints
def speak(text):
    length_of_text = len(str(text))
    if length_of_text == 0:
        pass
    else:
        colorama.init(autoreset=True)
        print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"J.A.R.V.I.S : {text}")
        driver.find_element(By.ID, "voicetext").clear()  # Clear text field
        driver.find_element(By.ID, "voicetext").send_keys(text)
        driver.find_element(By.ID, "vorlesenbutton").click()  # Corrected value attribute
        sleep_time = max(2, (length_of_text // 30) * 4 + 4)  # Calculate sleep time based on text length
        sleep(sleep_time)
