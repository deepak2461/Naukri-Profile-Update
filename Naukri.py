from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import random

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("Naukri_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Naukri Creds
usernamee = os.getenv("naukri_username")
passwordd = os.getenv("naukri_pwd")




# Function to send Telegram message
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=data)

def send_telegram_screenshot(photo_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    with open(photo_path, "rb") as photo:
        data = {"chat_id": TELEGRAM_CHAT_ID}
        files = {"photo": photo}
        
        response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            print("✅ Screenshot sent to Telegram successfully!")
        else:
            print(f"❌ Failed to send screenshot. Status Code: {response.status_code}, Response: {response.text}")


def human_delay():
    time.sleep(random.uniform(3, 5))


# Configure Selenium WebDriver
#chrome_options = Options()
ua = UserAgent()
random_user_agent = ua.random

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes due to limited /dev/shm space
chrome_options.add_argument("--window-size=1920,1080") 
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f"user-agent={random_user_agent}")

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver = uc.Chrome(headless=True)
try:
    # Step 1: Open Naukri.com
    driver.get("https://www.naukri.com/")
    #time.sleep(3)
    human_delay()
    driver.save_screenshot("open_naukri.png")
    print("Opened Naukri site")
    sc0 = "open_site.png"
    driver.save_screenshot(sc0) 
    send_telegram_screenshot(sc0)

    # Step 2: Click Login
    #login_button = driver.find_element(By.XPATH, "//a[text()='Login']")
    #login_button = driver.find_element_by_xpath('//*[@id="login_Layer"]')
    login_button = driver.find_element(by=By.XPATH, value='//*[@id="login_Layer"]')
    login_button.click()
    time.sleep(3)
    #driver.save_screenshot("login_click.png")
    sc1 = "login_click.png"
    driver.save_screenshot(sc1) 
    send_telegram_screenshot(sc1)
    print("Clicked on Login")

    # Step 3: Enter Creds
    #username = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div/div[2]/div/form/div[2]/input')
    username = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[4]/div[2]/div/div/div[2]/div/form/div[2]/input')
    #password = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div/div[2]/div/form/div[3]/input')
    password = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[4]/div[2]/div/div/div[2]/div/form/div[3]/input')
    username.send_keys(usernamee)
    password.send_keys(passwordd)
    password.send_keys(Keys.RETURN)
    time.sleep(5)
    print("Step 3 completed")

    # Step 4: Navigate to Profile Page
    driver.get("https://www.naukri.com/mnjuser/profile")
    time.sleep(5)

    #Close popup -- trying to clink anywhere on the screen
    #pop = driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div/div[1]')
    #pop.click()
    #time.sleep(2)
    
    # Step 5: Click Edit and Save
    #edit_button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/span/div/div/div/div/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div/div[1]/em')
    #edit_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/span/div/div/div/div/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div/div[1]/em')
    edit_button = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/span/div/div/div/div/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div/div[1]/em')
    edit_button.click()
    time.sleep(2)

    #save_button = driver.find_element(By.XPATH, "//*[@id="saveBasicDetailsBtn"]")
    #save_button = driver.find_element_by_xpath('//*[@id="saveBasicDetailsBtn"]')
    save_button = driver.find_element(by=By.XPATH, value='//*[@id="saveBasicDetailsBtn"]')
    save_button.click()
    time.sleep(3)

    # Success Message
    send_telegram_message("✅ Naukri Profile Update: SUCCESS")
    print("Profile updated successfully.")

except Exception as e:
    # Failure Message
    send_telegram_message(f"❌ Naukri Profile Update FAILED: {str(e)}")
    print("Error:", str(e))

finally:
    driver.quit() #commenting for testing purpose
    print("Done")
