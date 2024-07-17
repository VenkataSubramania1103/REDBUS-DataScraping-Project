import time
import pandas as pd 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from durations_nlp import Duration
from datetime import datetime

def firstPage():
    state_service = driver.find_elements(By.CSS_SELECTOR,"a[class='D113_link']")
    l=[]
    name=[]
    link=[]
    for state in state_service:
        name.append(state.text)
        link.append(state.get_attribute('href'))
    l.append(name)
    l.append(link)
    return l
    
def SecondPage(link):
    driver.get(link)
    driver.maximize_window()
    l=[]
    routes_available=[]
    routes_link=[]
    #driver.find_element(By.CSS_SELECTOR,"div[class='DC_117_pageTabs DC_117_pageActive']").click()
    current_page=driver.find_elements(By.CSS_SELECTOR,"a[class='route']")
    for page in current_page:
        routes_link.append(page.get_attribute('href'))
        routes_available.append(page.text)
    pages=driver.find_elements(By.CSS_SELECTOR,"div[class='DC_117_pageTabs ']")
    for i in pages:
        ActionChains(driver)\
            .click(i)\
            .perform()
        routes=driver.find_elements(By.CSS_SELECTOR,"a[class='route']")
        for r in routes:
            routes_link.append(r.get_attribute('href'))
            routes_available.append(r.text)
        time.sleep(5)
    l.append(routes_available)
    l.append(routes_link)
    return l

def finalPageScraping(name,link):
    driver.get(link)
    driver.maximize_window()
    time.sleep(1)
    b=driver.find_elements(By.CSS_SELECTOR,"div[class='button']")
    for i in range(len(b)-1,-1,-1):
        b[i].click()
    x=0
    l=[]
    while True:
        x=x+1
        driver.execute_script('scrollBy(0,100)')
        #time.sleep(0.5)
        if(x>1000):
            break
    bus_name=driver.find_elements(By.CSS_SELECTOR,"div[class='travels lh-24 f-bold d-color']")
    bus_type=driver.find_elements(By.CSS_SELECTOR,"div[class='bus-type f-12 m-top-16 l-color evBus']")
    bus_dept=driver.find_elements(By.CSS_SELECTOR,"div[class='dp-time f-19 d-color f-bold']")
    bus_dur=driver.find_elements(By.CSS_SELECTOR,"div[class='dur l-color lh-24']")
    bus_reach=driver.find_elements(By.CSS_SELECTOR,"div[class='column-five p-right-10 w-10 fl']")
    bus_star=driver.find_elements(By.CSS_SELECTOR,"div[class='column-six p-right-10 w-10 fl']")
    bus_price=driver.find_elements(By.CSS_SELECTOR,"div[class='fare d-block']")
    bus_seats=driver.find_elements(By.CSS_SELECTOR,"div[class='column-eight w-15 fl']")

    for i in range(len(bus_name)):
        bus_details=[]
        bus_details.append(name)
        bus_details.append(link)
        bus_details.append(bus_name[i].text)
        bus_details.append(bus_type[i].text)  
        bus_details.append(bus_dept[i].text)
        bus_details.append(bus_dur[i].text)
        bus_details.append(bus_reach[i].text.split('\n')[0])
        bus_details.append(bus_star[i].text.split('\n')[0])
        bus_details.append(bus_price[i].text)
        bus_details.append(bus_seats[i].text.split('\n')[0])
        l.append(bus_details)
    
    return l


driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://www.redbus.in/online-booking/rtc-directory')
driver.maximize_window()
time.sleep(5) # wait for some 5 sec
result=[]
f_page=firstPage()
for j in range(0,len(f_page[0])):
    second_page=SecondPage(f_page[1][j])
    for i in range(len(second_page[0])):
        l=finalPageScraping(second_page[0][i],second_page[1][i])
        for i in l:
            result.append(i)


cols=['Bus Route Name','Bus route link','Bus Name','Bus Type','Departing time','Duration','Reaching Time','Rating','Price','Seats available']
df = pd.DataFrame(result, columns=cols) 
df = df.drop_duplicates()
df['Departing time']=pd.to_datetime(df['Departing time']).dt.strftime('%Y-%m-%d %H:%M:%s')

df['Reaching Time']=pd.to_datetime(df['Reaching Time']).dt.strftime('%Y-%m-%d %H:%M:%s')

df['Price']=(df['Price'].str.replace('INR ', '')).astype(float)

df['Seats available']=df['Seats available'].str.replace(' Seats available','')
df['Seats available']=df['Seats available'].str.replace(' Seat available','')

df["Rating"]=df["Rating"].str.replace('New','')
df["Rating"]=df["Rating"].str.replace(' ','')
df["Rating"]=pd.to_numeric(df["Rating"]).fillna(0)
df["Seats available"]=pd.to_numeric(df["Seats available"])
df.to_excel("output_redbus.xlsx", index=False)
print("Extracted")