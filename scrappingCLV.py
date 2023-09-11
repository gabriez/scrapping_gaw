from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time

data = {
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
    data['address'].append(location[l].text)

for m in range(len(meters)):
    data['meters'].append(meters[m].text)

for p in range(len(price)):
    data['prices'].append(price[p].text)

#---------------------------------------
# The next resolution is for the images
#---------------------------------------

# This will move through the page so the webpage makes the proper requests to the server
elementToMove = driver.find_elements(By.CLASS_NAME, 'sc-1tt2vbg-3')
action = ActionChains(driver)
for element in elementToMove:
    action.move_to_element(element).perform()
    action.click(on_element = element).perform()
    driver.switch_to.window(driver.window_handles[0])

# Timer for letting the webpage load
time.sleep(25)


# Maybe this unnecesary, but is an explicit wait by Selenium for recording all the img elements
imagesRaw = WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="flickity-slider"]/child::img'))
    )

images = []
insideImage = []
for i in range(len(imagesRaw)):
    if (i + 1) % 8 != 0: 
        insideImage.append(imagesRaw[i].get_attribute('src') if imagesRaw[i].get_attribute('src') != None else imagesRaw[i].get_attribute('data-flickity-lazyload'))
    else:
        insideImage.append(imagesRaw[i].get_attribute('src') if imagesRaw[i].get_attribute('src') != None else imagesRaw[i].get_attribute('data-flickity-lazyload'))
        images.append(insideImage)
        insideImage = []


data['images'] = images

# for image in range(len(images)):
#     data['images'].append(images[image])

print(len(driver.window_handles))
for windowTo in range(len(driver.window_handles)): 
     print(windowTo)
     driver.switch_to.window(driver.window_handles[windowTo])
     if windowTo != 0: 
        print(driver.current_url, windowTo)
        data['url'].append(driver.current_url)  

# Exporting to Excel 

print(len(data['url']), len(data['images']), len(data['address']), len(data['meters']), len(data['prices']))

df = pd.DataFrame(data)   
customHeader = ['Precios', 'Metros cuadrados', 'Dirección', 'URL de las imágenes', "URL's"]

df.to_excel('lasLlaves.xlsx', na_rep='N/A', index=False, header = customHeader)