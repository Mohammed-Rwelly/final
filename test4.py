from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_jobs(keyword, num_jobs, verbose, slp_time):
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    chrome_options = Options()
    options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"]
    for option in options:
        chrome_options.add_argument(option)
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    driver.set_window_size(1120, 1000)
    url='https://www.glassdoor.com/Job/turkey-data-jobs-SRCH_IL.0,6_IN238_KO7,11.htm?clickSource=searchBox'
    #url ="https://www.glassdoor.com/Job/foster-city-ca-"+keyword+"-jobs-SRCH_IL.0,14_IC1163997_KO15,29.htm?src=GD_JOB_AD&srs=ALL_RESULTS&jl=1007891100315&ao=1136043&s=345&guid=00000181bfeda65bb92afaacd021b371&pos=101&t=SR-JOBS-HR&vt=w&cs=1_16d0396a&cb=1656782432051&jobListingId=1007891100315&jrtk=3-0-1g6vur9k4kcle801-1g6vur9kfjoqf800-76aaad84e43fcb11-"
    driver.get(url)
    print(num_jobs)
    
    #Let the page load. Change this number based on your internet speed.
    time.sleep(slp_time)
    #Test for the "Sign Up" prompt and get rid of it.
    try:
        element=driver.find_element(By.CLASS_NAME, "selected").click()
    except ElementClickInterceptedException:
        pass

    time.sleep(5)

    try:
        element=driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click()#clicking to the X.
        print(' x out worked')
     
    except NoSuchElementException:
        print(' x out failed')
    job_buttons1 = driver.find_elements(By.XPATH,"//*[@id='MainCol']/div[1]/ul/li")
    job_buttons = driver.find_elements(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li/div[2]/a')
   # print("job_post = ",len(job_buttons1))
   # print("job_href = ",len(job_buttons))
    job=[]
    for i in range(3):
       # print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
        job_buttons1[i].click()  #You might
        print(job_buttons[i].get_attribute("href"))
        time.sleep(10)
        collected_successfully = False
        print('start')
        try:
            element=driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click()#clicking to the X.
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed')
        try:
            jobbbb=driver.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li[{}]/div[2]/div[3]/div[2]/div[2]'.format(i+1)).text
        except NoSuchElementException:
            jobbbb=driver.find_element(By.XPATH,'//*[@id="MainCol"]/div[1]/ul/li[{}]/div[2]/div[2]/div/div[2]'.format(i+1)).text
            #print("وينهااااااااااااااااااا")
            pass
            
        job.append({"job_id":jobbbb})
    return pd.DataFrame(job)                    
 
df=get_jobs('Data Scientist', 2, False, 10)
df.to_csv("data_final.csv",index=True) 


