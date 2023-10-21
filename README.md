# image_dataset_collector
this script will help automate the image collection process from Qwant images  using Selenium
## requirments
- Install the requirements
```
pip -r install requirements.txt
```

- Mozilla firefox browser https://www.mozilla.org/en-US/firefox/new/
- download geckodriver https://github.com/mozilla/geckodriver/releases
## How to use the script 
- run ```python dataset_collector.py "query" folder_name```
where query represents the search keyword and the folder_name represents the name of the local folder where your images would be saved



PS: because the default mode that's used in the code is headless, the browser will only appear in the task manager and won't open up, this is in order to save up on some resources and make the process a bit faster
