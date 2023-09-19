from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import threading


#------------------------------------------------------THREAD-----------------------------------

def threadInfo(baseUrl): 
    optionsThread = webdriver.ChromeOptions()
    optionsThread.add_argument("--headless")
    print(baseUrl)
    driver = webdriver.Chrome(options = optionsThread)
    driver.get(baseUrl)

    
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
    imagesRaw =  explicitWaitThread.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="gallery tile-5 normal"]/descendant::img')))
    for i in range(len(imagesRaw)):
        imagesRaw[i] = imagesRaw[i].get_attribute('src')
    images.append(imagesRaw)


#-----------------------------------------------------------------------------------------------


BASEURL = 'https://www.century21global.com/en/l/a/venezuela,miranda,caracas?page=1&max=48'


options = webdriver.ChromeOptions()
options.add_argument("--headless")


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

    td = threading.Thread(target=threadInfo, args=(container.get_attribute('href'),))
    td.start()

    td.join()
    # action.move_to_element(container).perform()
    # action.context_click(container).perform()
    # press('enter', presses=2)
    # driver.switch_to.window(driver.window_handles[1])
    
    # Getting size, url, location and price 
           
    # sizeRaw = explicitWait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="main-content"]/site-property/div[1]/div[2]/div/div[2]/div[2]/dl/dd/span[1]')))
    # priceRaw = explicitWait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="mat-display-2 fw-bold mb-2 d-flex ng-star-inserted"]')))
    # locationRaw = explicitWait.until(EC.visibility_of_element_located((By.XPATH, '//*[@class="mat-h4 mb-0 ng-star-inserted"]')))
    # size.append(sizeRaw.text)
    # prices.append(priceRaw.text)
    # url.append(driver.current_url)
    # location.append(locationRaw.text)


    # # Getting images
    # time.sleep(3)
    # imagesRaw =  explicitWait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="gallery tile-5 normal"]/descendant::img')))
    # for i in range(len(imagesRaw)):
    #     imagesRaw[i] = imagesRaw[i].get_attribute('src')
    # images.append(imagesRaw)
    # print(len(imagesRaw), len(prices), len(url), len(location), len(size))
    # driver.close()
    # driver.switch_to.window(driver.window_handles[0])


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