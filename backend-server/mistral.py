from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from fuzzywuzzy import fuzz
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import os
import chromedriver_autoinstaller as chromedriver

# Initialize Spacy model
nlp = spacy.load('en_core_web_md')

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
        print(self.driver.capabilities['browserVersion'])

    def init(self):
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

def get_response(question, driver_manager):
    driver = driver_manager.get_driver()
    response = ""

    try:
        input_box = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Ask anything!']")
        input_box.send_keys(question)

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Send question']")
        
        while submit_button.get_attribute("disabled"):
            time.sleep(1)  # Wait for 1 second before checking again
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Send question']")

        submit_button.click()
        time.sleep(15)
        
        response_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'prose') and contains(@class, 'select-text')]")
        response = response_elements[-1].text  # Get the text of the last response element
    except Exception as e:
        print(e)

    return response

def fuzzy_matching_score(response, expected_answer):
    return fuzz.ratio(response, expected_answer)

def cosine_similarity_spacy_score(response, expected_answer):
    doc1, doc2 = nlp(expected_answer), nlp(response)
    vector1 = doc1.vector
    vector2 = doc2.vector
    cosine_sim = cosine_similarity([vector1], [vector2])
    return cosine_sim[0][0].item()