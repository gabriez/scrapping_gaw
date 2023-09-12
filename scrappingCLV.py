from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time

lasLlavesData = {
    'prices': [], 
    'meters': [], 
    'address': [],
    'images': [],
    'url': []
}
baseUrl = "https://www.conlallave.com/inmuebles-en-venta-en-area-metropolitana-caracas.html"

driver = webdriver.Chrome()
driver.get(baseUrl)

price = driver.find_elements(By.CLASS_NAME,'sc-12dh9kl-4')
meters = driver.find_elements(By.XPATH, '//img[@class="sc-1uhtbxc-1 eLhfrW"]/following::span[1]')
location = driver.find_elements(By.CLASS_NAME, 'sc-ge2uzh-1')

for l in range(len(location)):
    lasLlavesData['address'].append(location[l].text)

for m in range(len(meters)):
    lasLlavesData['meters'].append(meters[m].text)

for p in range(len(price)):
    lasLlavesData['prices'].append(price[p].text)

#---------------------------------------
# The next resolution is for the images
#---------------------------------------

# This will move through the page so the webpage makes the proper requests to the server
elementToMove = driver.find_elements(By.CLASS_NAME, 'sc-i1odl-3')
action = ActionChains(driver)

counter = 0

while counter < len(elementToMove):
    action.move_to_element(elementToMove[counter]).perform()
    if len(driver.window_handles) < 2:
        action.click(on_element = elementToMove[counter]).perform()
        if len(driver.window_handles) == 2:
            driver.switch_to.window(driver.window_handles[1])
            lasLlavesData['url'].append(driver.current_url)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        else:    
            counter -= 1
    counter += 1
        
# Timer for letting the webpage load
time.sleep(5)

# Maybe this unnecesary, but is an explicit wait by Selenium for recording all the img elements
imagesContainers = WebDriverWait(driver, 15).until(
     EC.presence_of_all_elements_located((By.CLASS_NAME, 'flickity-slider'))
     )

images = []
for imagesGroup in imagesContainers:
    imagesRaw = imagesGroup.find_elements(By.TAG_NAME, 'img')
    for i in range(len(imagesRaw)):
        imagesRaw[i] = imagesRaw[i].get_attribute('src') if imagesRaw[i].get_attribute('src') != None else imagesRaw[i].get_attribute('data-flickity-lazyload')
    images.append(imagesRaw)


lasLlavesData['images'] = images

# Exporting to CSV 
df = pd.DataFrame(lasLlavesData)   
customHeader = ['Precios', 'Metros_cuadrados', 'Dirección', 'URL_de_las_imágenes', "URLs"]

df.to_csv('lasLlaves.csv', na_rep='N/A', index=False, header = customHeader)