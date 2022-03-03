# image_dataset_collector
this script will help automate the image collection process from Qwant images  using Selenium
## requirments
- Install Selenium  
```
pip install selenium
```
- Install urllib3
```
pip install urllib3
```
- Install Beautifulsoup
```
pip install bs4
```
- Mozilla firefox browser https://www.mozilla.org/en-US/firefox/new/
- download geckodriver https://github.com/mozilla/geckodriver/releases
## How to use the script 
1) run python dataset_collector.py through your commandline
2) type down your query 
3) type down the folder name to store your results 


PS: because the default mode that's used in the code is headless , the browser will only appear in task manager and won't open up , this is in order to save up on some ressources and make the process a bit faster
