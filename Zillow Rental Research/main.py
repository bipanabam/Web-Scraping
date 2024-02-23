import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSf0AxB-6wLFrza3GlyWHp1y5vXTM-Swv_7EII3GMKQqSVqDDQ/viewform" \
            "?usp=sf_link"

ZILLOW_LINK = "https://www.zillow.com/san-francisco-ca/rentals/" \
              "?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.6259330649414%2C%22east%22%3A-122.2407249350586%2C%22south%22%3A37.64573520729978%2C%22north%22%3A37.904621063717464%7D%2C%22mapZoom%22%3A11%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22price%22%3A%7B%22min%22%3Anull%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3Anull%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%2C%22max%22%3Anull%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%7D%5D%7D"
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}


# Scraping all the listings from the Zillow web address using Beautiful Soup
response = requests.get(ZILLOW_LINK, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

all_addresses = [address.getText().split(" | ")[-1] for address in soup.select(selector="address")]
print(len(all_addresses))

all_links = []
link_elements = soup.select(selector=".property-card-data a")
for link in link_elements:
    href = link.get("href")
    if href.startswith("/"):
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(link.get("href"))


all_prices = []
price_elements = soup.select(selector=".property-card-data div div span")
for price in price_elements:
    price_text = price.getText()
    if "+" in price_text:
        all_prices.append(price_text.split("+")[0])
    else:
        all_prices.append(price_text.split("/")[0])


# Using Selenium to fill in the form(SF Renting Research)
chrome_driver_path = "your-chromedriver-absolute-path"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

for n in range(len(all_links)):
    driver.get(FORM_LINK)

    time.sleep(2)
    address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]'
                                            '/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/'
                                          'div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]'
                                         '/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    address.send_keys(all_addresses[n])
    price.send_keys(all_prices[n])
    link.send_keys(all_links[n])
    submit_button.click()

