# TODO: choice between URL or keywords
import bs4
from selenium import webdriver
import urllib3
from urllib3 import PoolManager
import logging
import warnings
import os
from os import makedirs
from os.path import isdir,join
from random import random
from time import sleep,perf_counter
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

query = input('choose something to look up ...\n').split()
https = PoolManager()

folder_name = input('choose a folder name for your dataset \n')
if not isdir(folder_name):
	#if the folder doesnt exist , create one
	makedirs(folder_name)

def download_image(url):
	# first we start by sending a an HTTP request to make sure all is good
	response = https.request('GET', url) 
	if response.status == 200:
		with open(join(folder_name, str(random())+".jpg"), 'wb') as file:
			file.write(response.data)
			
	else:
		sleep(0.5)
		warnings.warn("Warning , couldn't download this image , moving on the the next one ...")



def create_query(keywords):
	
	'''takes the keyword list based on input and the basic Qwant query,returns a url as a string'''

	qwant_url='https://www.qwant.com/?l=en&q='
	query = '+'.join(keywords)
	search_URL=''.join([qwant_url,query,'+-gif&t=images'])
	
	
	
	return search_URL

search_URL = create_query(query)
#you can change your driver path accordingly
driver_path = 'geckodriver.exe'
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless=True
#fireFoxOptions.set_headless()
driver = webdriver.Firefox(executable_path=driver_path,options=fireFoxOptions)

try:
	driver.get(search_URL)
except:
	print("try another query")

page_html = driver.page_source

pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
# find the image containers to loop through them

containers = pageSoup.findAll('a', {'class':"Images-module__ImagesGridItem___1W4Bs"} )
	
previews = [driver.find_element_by_css_selector(f'a.Images-module__ImagesGridItem___1W4Bs:nth-child({i}) > div:nth-child(1) > img:nth-child(1)') for i in range(1,len(containers))]


imageURL = [element.get_attribute('src') for element in previews]

assert len(imageURL) != 0 ,"There are no  URLS to download"

t1=perf_counter()
# multithreading highly improves the performance
with ThreadPoolExecutor() as executor:
	executor.map(download_image,imageURL)
t2=perf_counter()

print(f'it took {t2-t1} seconds to download {len(imageURL)} images')
