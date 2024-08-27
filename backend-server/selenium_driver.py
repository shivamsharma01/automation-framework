import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller as chromedriver

class DriverManager:
    def __init__(self):
        chromedriver.install(no_ssl=True)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://chat.mistral.ai/login")
        
        time.sleep(2)
        
        try:
            email_input = self.driver.find_element(By.ID, ":R35l3:")
            email_input.send_keys(os.environ['username'])
            
            password_input = self.driver.find_element(By.ID, ":R55l3:")
            password_input.send_keys(os.environ['password'])
            
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'][value='password']")
            submit_button.click()
            time.sleep(5)

            self.driver.get("https://chat.mistral.ai/chat")
            time.sleep(2)
        except Exception as e:
            print(e)
            self.driver.quit()
        

    def close(self):
        self.driver.quit()

    def get_driver(self):
        return self.driver
    
    def get_question_response(self, question):
        try:
            input_box = self.driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Ask anything!']")
            input_box.send_keys(question)

            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Send question']")
            
            while submit_button.get_attribute("disabled"):
                time.sleep(1)
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Send question']")

            submit_button.click()
            time.sleep(15)
            
            response_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'prose') and contains(@class, 'select-text')]")
            return response_elements[-1].text
        except Exception as e:
            print(e)
            return ""
    
