import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# Load the Excel file
df = pd.read_excel('contacts.xlsx')

# Initialize the Selenium WebDriver (assuming Chrome)
driver = webdriver.Chrome()  # Update with the path to your chromedriver
driver.get("https://web.whatsapp.com")

# Wait for the user to scan the QR code
input("Press Enter after scanning the QR code in WhatsApp Web")

def open_group_chat(group_name):
    # Search for the group chat
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.clear()
    search_box.send_keys(group_name)
    time.sleep(3)  # Wait for search results
    search_box.send_keys(Keys.ENTER)

def search_contact(phone_number):
    # This is where we search for a contact to add
    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.clear()
    search_box.send_keys(phone_number)
    time.sleep(3)  # Allow some time for search results to appear
    search_box.send_keys(Keys.ENTER)

def add_contact_to_group():
    # Click on the group info to open the group settings
    group_info_button = driver.find_element(By.XPATH, '//header[@data-testid="conversation-header"]//span[@data-testid="menu"]')
    group_info_button.click()
    time.sleep(2)

    # Click 'Add participant' button
    add_participant_button = driver.find_element(By.XPATH, '//div[contains(text(), "Add participant")]')
    add_participant_button.click()
    time.sleep(2)

    # Click the add button to add the contact to the group
    driver.find_element(By.XPATH, '//span[contains(text(), "Add")]').click()

# Open the group chat
open_group_chat("KKE Kader - Alle Kompanien")
time.sleep(5)  # Wait for the chat to open

# Iterate through the Excel data and add each contact
for index, row in df.iterrows():
    phone_number = row['Telefonnummer']
    print(f"Adding contact: {phone_number}")
    search_contact(phone_number)
    add_contact_to_group()
    time.sleep(5)  # Wait before processing the next contact

# Close the WebDriver when done
driver.quit()