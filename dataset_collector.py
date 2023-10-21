import bs4
from utility import *
from selenium import webdriver
from urllib3 import PoolManager
import warnings
from os import makedirs
import argparse
import urllib.request
from os.path import isdir,join
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
https = PoolManager()
# attempt to make a connection 
connect()
parser = argparse.ArgumentParser(description='Image Scraper')
parser.add_argument('query', type=str, help='Query to search for images')
parser.add_argument('folder', type=str, help='Folder to store images')
args = parser.parse_args()
query = args.query.split()

if query==[]:
	raise ValueError('Empty string passed as query')

folder_name = args.folder
if folder_name=='':
	raise ValueError('Empty string passed as folder name')
elif not isdir(folder_name):
	#if the folder doesnt exist , create one
	makedirs(folder_name)
gen=(i for i in range(0,1000000))


# you can change your driver path accordingly
try:

	s = Service('geckodriver.exe')
except:
	raise Exception('Error, couldnt load the geckodriver , please check the path')
try:
	driver = webdriver.Firefox(service=Service('geckodriver.exe'), options=options)
	#driver = webdriver.Firefox(service=s)
except:
	raise Exception('Error initializing the webdriver')

search_URL = create_query(query)
driver.get(search_URL) # look up the query


imageURLS=[driver.find_element(by=By.CSS_SELECTOR,value=f'a._1W4Bs:nth-child({i}) > div:nth-child(1) > img:nth-child(1)').get_attribute('src') for i in range(1,51)]

if len(imageURLS)==0:
	raise Exception("Couldn't find any images , try another query")
def download_image(url):

    """this function downloads the image and saves it to disk"""
	# first we start by sending a an HTTP request to make sure all is good
    response = https.request('GET', url) 
    if response.status == 200:
	    with open(join(folder_name, str(f"{''.join(query)}_{next(gen)}")+".jpg"), 'wb') as file:
		    file.write(response.data)
			
    else:
	    warnings.warn("Warning , couldn't download this image , moving on the the next one ...")	
# multithreading highly improves the performance
t1=perf_counter()
with ThreadPoolExecutor() as executor:
	executor.map(download_image,imageURLS)

t2=perf_counter()
print(f'it took {t2-t1} seconds to download {len(imageURLS)} images')
driver.quit()