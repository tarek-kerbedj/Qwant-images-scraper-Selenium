##TODO: choice between URL or keywords
import bs4
import requests
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
query= input('choose something to look up ...\n').split()
folder_name = input('choose a file name for your dataset \n')
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)

def download_image(url, folder_name, num):

	
    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)


def create_query(keywords,url='https://www.qwant.com/?l=en&q='):
	'''takes the keyword list based on input and the basic Qwant query,returns a url as a string'''
	query = '+'.join(keywords)
	search_URL = url + query + '+-gif&t=images'
	return search_URL




search_URL=create_query(query)

driver_path='geckodriver.exe'
driver=webdriver.Firefox(executable_path=driver_path)



wait = WebDriverWait(driver, 10)

driver.get(search_URL)
page_html = driver.page_source

pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('a', {'class':"Images-module__ImagesGridItem___1W4Bs"} )

len_containers=len(containers)
for i in range(2, len_containers+1):

	preview=driver.find_element_by_css_selector(f'a.Images-module__ImagesGridItem___1W4Bs:nth-child({i}) > div:nth-child(1) > img:nth-child(1)')

	preview.click()
	imageURL=preview.get_attribute('src')
	try:
		download_image(imageURL, folder_name, i)
		print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
	except:
		print("Couldn't download an image %s, continuing downloading the next one"%(i))
