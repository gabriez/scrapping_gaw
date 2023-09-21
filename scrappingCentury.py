from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Variables that will store all the information scraped
images = []
prices = []
size = []
url = []
location = []

BASEURL = 'https://www.century21global.com/en/l/a/venezuela,miranda,caracas?page=1&max=48'
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless=new")


driver = webdriver.Chrome(options = options)
driver.get(BASEURL)

action = ActionChains(driver)
explicitWait = WebDriverWait(driver, 10)


# Getting info to manipulate URL
maxPerPage = driver.find_element(By.XPATH, '//*[@class="d-none d-lg-flex justify-content-start align-items-center"]/div[1]/button[last()]') # This sets the pagination in the website, so I can get the info of all the pages that will be scraped
action.click(on_element = maxPerPage).perform()
pages = int(driver.find_element(By.XPATH, '//*[@class="d-flex justify-content-start align-items-center ng-star-inserted"]/button[last()-1]').text) # This returns the element that contains the information about the quantity of pages

i = 1

while i <= pages: 
    j = 1
    if i > 1:
        dynamicUrl = f'https://www.century21global.com/en/l/a/venezuela,miranda,caracas?page={i}&max=48'
        driver.get(dynamicUrl)
        time.sleep(1)    
    containersPages = explicitWait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="col-lg-6 col-xl-4 ng-star-inserted"]/site-property-thumbnail/a')))    
    print(len(containersPages))
    for container in containersPages: 
        baseUrl = container.get_attribute('href')
        print(baseUrl, j)
        driver.get(baseUrl)
        time.sleep(1)
        
        try:
            sizeRaw = explicitWait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="main-content"]/site-property/div[1]/div[2]/div/div[2]/div[2]/dl/dd/span[1]'))) 
        except:
            sizeRaw = explicitWait.until(EC.visibility_of_element_located((By.XPATH, '//site-property/div[1]/div[2]/div/div[2]/div[1]/dl/dd'))) 
        priceRaw = explicitWait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="mat-display-2 fw-bold mb-2 d-flex ng-star-inserted"]')))
        locationRaw = explicitWait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="mat-h4 mb-0 ng-star-inserted"]')))
        size.append(sizeRaw.text)
        prices.append(priceRaw.text)
        url.append(driver.current_url)
        location.append(locationRaw.text)

        # Getting images
        time.sleep(1)
        imagesRaw =  explicitWait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="gallery-wrapper ng-star-inserted"]/descendant::img')))
        for i in range(len(imagesRaw)):
            imagesRaw[i] = imagesRaw[i].get_attribute('src')
        images.append(imagesRaw)
        driver.back()
        j += 1
    i += 1



data = {
    "prices": prices,
    "size": size,
    "location": location,
    "images": images,
    "url": url
}

df = pd.DataFrame(data)
customHeader = ['Precios', 'Metros_cuadrados', 'Dirección', 'URL_de_las_imágenes', "URLs"]
df.to_csv('Century.csv', na_rep='N/A', index=False, header = customHeader)
