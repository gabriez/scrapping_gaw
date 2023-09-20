from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import threading


#------------------------------------------------------THREAD-----------------------------------

#-----------------------------------------------------------------------------------------------


BASEURL = 'https://www.century21global.com/en/l/a/venezuela,miranda,caracas?page=1&max=48'


options = webdriver.ChromeOptions()
#options.add_argument("--headless")


driver = webdriver.Chrome(options = options)
driver.get(BASEURL)

action = ActionChains(driver)
explicitWait = WebDriverWait(driver, 10)
time.sleep(3)

containersPages = explicitWait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="col-lg-6 col-xl-4 ng-star-inserted"]/site-property-thumbnail/a')))

global images
global prices
global size
global url
global location

images = []
prices = []
size = []
url = []
location = []

# '//*[@class="col-lg-6 col-xl-4 ng-star-inserted"]'
#'//*[@class="col-lg-6 col-xl-4 ng-star-inserted"]/site-property-thumbnail/a/div/div/div[2]/div[4]/div[3]/span'


for container in containersPages: 
    # time.sleep(2)
    # action.click(on_element = container).perform()
    # time.sleep(2)
    # driver.back()

    baseUrl = container.get_attribute('href')
    print(baseUrl)
    driver.get(baseUrl)
    time.sleep(1)
    
    explicitWaitThread = WebDriverWait(driver, 10)
    try:
        sizeRaw = driver.find_element(By.XPATH, '//*[@class="main-content"]/site-property/div[1]/div[2]/div/div[2]/div[2]/dl/dd/span[1]') 
    except:
        sizeRaw = driver.find_element(By.XPATH, '//site-property/div[1]/div[2]/div/div[2]/div[1]/dl/dd') 
    priceRaw = explicitWaitThread.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="mat-display-2 fw-bold mb-2 d-flex ng-star-inserted"]')))
    locationRaw = explicitWaitThread.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="mat-h4 mb-0 ng-star-inserted"]')))
    size.append(sizeRaw.text)
    prices.append(priceRaw.text)
    url.append(driver.current_url)
    location.append(locationRaw.text)

    # Getting images
    time.sleep(2)
    imagesRaw =  explicitWaitThread.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="gallery-wrapper ng-star-inserted"]/descendant::img')))
    for i in range(len(imagesRaw)):
        imagesRaw[i] = imagesRaw[i].get_attribute('src')
    images.append(imagesRaw)
    driver.back()



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

#//*[@class="row g-4 py-3 layout-grid"]