from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
import random

'''
import requests
import urllib
from bs4 import BeautifulSoup
from os.path import join
from os import makedirs
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
options = webdriver.ChromeOptions()
options.add_argument('--headless')
# Initialize the WebDriver (make sure you have ChromeDriver installed)
driver = webdriver.Chrome()

# Open the webpage
web_url = input("web: ")
driver.get(web_url)

# Scroll down to load images (you may need to adjust the number of scrolls)
time.sleep(5)
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for images to load

# Find image elements
image_elements = driver.find_elements(By.CSS_SELECTOR, "div.page-chapter img.lozad ")
print(image_elements)
# Download each image
user_agent_list = [
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
   "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.99 Mobile/15E148 Safari/604.1"
]
reffer_list=[
   'https://nettruyenco.vn/'
]
headers = {
   'Connection': 'keep-alive',
   'Cache-Control': 'max-age=0',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': random.choice(user_agent_list),
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
   'referer': random.choice(reffer_list)
}
for index, img_element in enumerate(image_elements):
    img_url = img_element.get_attribute("src")
    #response = requests.Session()
    #response.headers.update({'referer': "https://nettruyenco.vn/"})
    response = requests.get(img_url, headers=headers)
    with open(f"image_{index}.png", "wb") as f:
        f.write(response.content)

# Close the WebDriver
driver.quit()