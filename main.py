from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

business = "barber"
zip_code = "30543"
filename = "data.csv"
link = f"https://www.google.com/maps/search/{business}+in+{zip_code}/"

browser = webdriver.Chrome()
record = []

def Selenium_extractor():
    action = ActionChains(browser)
    wait = WebDriverWait(browser, 10)  # Adjust timeout as needed
    
    browser.get(str(link))
    time.sleep(10)
    
    try:
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        len_a = len(a)

        for i in range(100):
            scroll_origin = ScrollOrigin.from_element(a[i])
            action.scroll_from_origin(scroll_origin, 0, 100).perform()
            action.move_to_element(a[i]).perform()
            
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "hfpxzc")))
            a[i].click()

            time.sleep(2)  # Adjust as needed
            source = browser.page_source
            soup = BeautifulSoup(source, 'html.parser')
            
            # Extract text from the specified XPath
            xpath = "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]"
            
            popup_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            popup_text = popup_element.text
            print("Text from popup:", popup_text)
            record.append(popup_text)  # Append extracted text to record list
            
            # Go back to clicking through the list
            # browser.back()
            time.sleep(5)  # Add a delay before proceeding to the next iteration
            a = browser.find_elements(By.CLASS_NAME, "hfpxzc")
            print(f"The length of the record is: {len(record)}")
    
    except Exception as e:
        print("An error occurred:", e)
        pass

# Perform scraping
Selenium_extractor()

# Create DataFrame from record list
df = pd.DataFrame({"Text": record})

# Export DataFrame to CSV file
df.to_csv(filename, index=False)

print("Data saved to", filename)
