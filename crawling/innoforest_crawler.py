import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

def init_driver(headless=True):
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    
    if headless:
        options.add_argument("--headless=new")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f"user-agent={user_agent}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Anti-bot bypass (removing webdriver flag via CDP)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
        """
    })
    return driver

def run_innoforest_crawler(email, password, target_url):
    print("[*] Init Innoforest Crawler...")
    driver = init_driver(headless=True) # Run in background
    try:
        login_url = "https://www.innoforest.co.kr/login"
        driver.get(login_url)
        time.sleep(random.uniform(2.0, 3.5)) # Human-like delay
        wait = WebDriverWait(driver, 15)
        
        print("[*] Attempting to login...")
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        pwd_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        
        email_field.send_keys(email)
        pwd_field.send_keys(password)
        
        # Click login button safely using Javascript execution to avoid ElementNotInteractableException
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/main/div[2]/div/div/form/div[4]/button/div')))
        driver.execute_script("arguments[0].click();", login_button)
        time.sleep(random.uniform(3.0, 5.0)) 

        print("[*] Navigating to target url...")
        driver.get(target_url)
        time.sleep(random.uniform(1.5, 3.0))
        
        company_info_name = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/div[2]/div[1]/div/div[1]/div[1]/div[2]/h1/span'))
        ).text
        representative_name = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="rightWrap"]/div[1]/div[2]/ul/li/div'))
        ).text

        print("-------------------------------")
        print(f"✅ [Target Captured] 기업명: {company_info_name}")
        print(f"✅ [Target Captured] 대표명: {representative_name}")
        print("-------------------------------")

    except Exception as e:
        print(f"❌ [Error] Crawling failed: {e}")
    finally:
        driver.quit()
        print("[*] Crawler Shutting Down.")

if __name__ == "__main__":
    run_innoforest_crawler(
        email="eudaimon125@hufs.ac.kr",
        password="Getajob8282$$", 
        target_url="https://www.innoforest.co.kr/company/CP00010087/%EB%A0%88%EB%B8%8C%EC%9E%87"
    )
