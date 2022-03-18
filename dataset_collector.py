import bs4
from selenium import webdriver
from urllib3 import PoolManager
import warnings
from os import makedirs
from os.path import isdir,join
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import urllib.request
https = PoolManager()
def connect(host='http://qwant.com'):
	'''checks for internet connectivity and availability of the website'''
	try:
		urllib.request.urlopen(host) 
		print('Connection succesful to Qwant.com ...')
		return True
	except:
		raise Exception("Unable to connect to Qwant.com , please make sure you're connected\
		or that Qwant.com isn't down")
connect()

query = input('choose something to look up ...\n').split()
if query==[]:
	raise ValueError('Empty string passed as query')


folder_name = input('choose a folder name for your dataset \n')

if folder_name=='':
	raise ValueError('Empty string passed as folder name')
elif not isdir(folder_name):
	#if the folder doesnt exist , create one
	makedirs(folder_name)

def download_image(url):
	# first we start by sending a an HTTP request to make sure all is good
	response = https.request('GET', url[0]) 
	if response.status == 200:
		with open(join(folder_name, str(url[1])+".jpg"), 'wb') as file:
			file.write(response.data)
			
	else:
		warnings.warn("Warning , couldn't download this image , moving on the the next one ...")



def create_query(keywords):
	
	'''takes the keyword list based on input and the basic Qwant query,returns a url as a string'''

	qwant_url='https://www.qwant.com/?l=en&q='
	query = '+'.join(keywords)
	search_URL=''.join([qwant_url,query,'+-gif&t=images'])
	return search_URL

s = Service('geckodriver.exe') # you can change your driver path accordingly
driver = webdriver.Firefox(service=s)

search_URL = create_query(query)
driver.get(search_URL) # look up the query

page_html = driver.page_source # get the page source code

pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')

containers = pageSoup.findAll('a', {'class':"Images-module__ImagesGridItem___1W4Bs"} ) # find the image containers to loop through them

# i stored a list of tuples that consist of an image URL and a corresponding index which i'll use to name the images	
imageURL = [(driver.find_element(by=By.CSS_SELECTOR,\
	value=f'a.Images-module__ImagesGridItem___1W4Bs:nth-child({i}) > div:nth-child(1) > img:nth-child(1)').get_attribute('src'),i)\
	 for i in range(1,len(containers))]

if len(imageURL)==0:
	raise Exception("Couldn't find any images , try another query")
	
# multithreading highly improves the performance
t1=perf_counter()
with ThreadPoolExecutor() as executor:
	executor.map(download_image,imageURL)
t2=perf_counter()
print(f'it took {t2-t1} seconds to download {len(imageURL)} images')
