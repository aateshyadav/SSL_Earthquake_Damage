
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def automate_codeaurorix():
    """
    Automates interactions with the CodeAurorix website:
    1. Opens the homepage.
    2. Scrolls to the bottom.
    3. Extracts and prints all services.
    4. Takes a screenshot.
    """
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    url = "https://codeaurorix.com"
    
    try:
        print(f"Opening the homepage: {url}")
        driver.get(url)
        
        driver.maximize_window()
        
        time.sleep(3)

        print("Scrolling to the bottom of the page...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)

        print("\nExtracting the list of services...")
        
        service_elements = driver.find_elements(By.CSS_SELECTOR, "div.service-card h5")
        
        # Check if any services were found.
        if service_elements:
            print("--- Services Offered by CodeAurorix ---")
            for index, service in enumerate(service_elements, start=1):
                print(f"{index}. {service.text}")
            print("--------------------------------------")
        else:
            print("Could not find any services on the page.")

        screenshot_filename = "homepage_screenshot.png"
        driver.save_screenshot(screenshot_filename)
        print(f"\nSuccessfully captured a screenshot: '{screenshot_filename}'")

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        print("Closing the browser.")
        driver.quit()

if __name__ == "__main__":
    automate_codeaurorix()