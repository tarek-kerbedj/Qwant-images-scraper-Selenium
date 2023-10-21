import urllib.request
def connect(host='http://qwant.com'):
	'''checks for internet connectivity and availability of the website'''
	try:
		urllib.request.urlopen(host) 
		print('Connection succesful to Qwant.com ...')
		return True
	except:
		raise Exception("Unable to connect to Qwant.com , please make sure you're connected\
		or that Qwant.com isn't down")
def create_query(keywords):
	
	'''takes the keyword list based on input and the basic Qwant query,returns a url as a string'''

	qwant_url='https://www.qwant.com/?l=en&q='
	query = '+'.join(keywords)
	search_URL=''.join([qwant_url,query,'+-gif&t=images'])
	return search_URL
