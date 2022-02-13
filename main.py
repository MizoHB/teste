#library


import selenium #importing selenium and the necessary options options to login to FB
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
#importing time libraries to add wait times 
import datetime
from time import sleep
#importing beautiful soup to read the page html source code  
from bs4 import BeautifulSoup
#to create csv file where we'll scrape the content
import pandas as pd
#requests for call ur phone using script sinch
import requests
#pywhatkit for send msg whatssap


#lists
content_list=[]
time_list=[]
name_list=[]
old_time = time_list

# regoniste if you have new poste


#get facebook page
def get_page_fb():
    chrome_options = Options()# we'll also add the options functionality to disable notifications
    chrome_options.add_argument("--disable-notifications")# disable notifications
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    driver.get("https://www.facebook.com")
    driver.maximize_window()
    sleep(2)
    #accept cookies
    #cookies = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="_42ft _4jy0 _9o-t _4jy3 _4jy1 selected _51sy"]'))).click()
    # email=driver.find_element_by_id("email")
    # email.send_keys("hamza.bg.77")        
    # password=driver.find_element_by_id("pass")
    # password.send_keys("Hamza__01")
    # sleep(1)
    # login=driver.find_element_by_name("login")
    # login.click()
    # sleep(2)
    driver.get("https://www.facebook.com/1337FutureIsLoading") # change group here
    sleep(4)
    while True:
        soup=BeautifulSoup(driver.page_source,"html.parser")
        all_posts=soup.find_all("div",{"class":"du4w35lb k4urcfbm l9j0dhe7 sjgh65i0"})
        for post in all_posts:
            try:#jsc_c_8q > span > a > strong > span
                name=post.find("a> strong > span").get_text()
            except:
                name="not found"
            print(name)
            try:
                content=post.find("div",{'dir':'auto'}).get_text()
            #except: to make sure that the code goes on even if there's nothing
            except:
                content="not found"
            print(content)
            try:
                time=post.find("a",{"class":"oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw"}).get("aria-label")
                print(time,)
            except:
                time="not found"
                
            content_list.append(content)
            time_list.append(time)
            name_list.append(name)
            df=pd.DataFrame({"name":name_list,"content":content_list,"time":time_list})
            df.drop_duplicates(subset ="content",keep = "first", inplace = True)
            df.to_csv("facebookdata2.csv") #change the filename here

            if df.shape[0]>1: #by default, you'll get 10 posts, but if you want more or less, change the number here
                break
        if df.shape[0]>1:
            break
        sleep(5)
        y = 500
        for timer in range(0, 2):
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 500
            sleep(3)
        driver.close()      
    print("______________________")
    print(time)

#if script find New poste call your phone
def call_phone():
    url = "https://calling.api.sinch.com/calling/v1/callouts"
    payload="{\n  \"method\": \"conferenceCallout\",\n  \"conferenceCallout\": {\n    \"cli\": \"+447520651168\",\n    \"destination\": {\n      \"type\": \"number\",\n      \"endpoint\": \"+212623889623\"\n    },\n   \"locale\": \"en-US\",\n    \"greeting\": \"\",\n    \"conferenceId\": \"4yl70aourhh\"\n  }\n}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic Mjk3MDRkZDgtM2U1OC00OGJjLTg0MDQtZGJiOWIzNmY3NmI5OmtTY05GWVF1a2tlTnlIZC8wSEhZR3c9PQ=='
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())

#send watssap msg if code working or not
def whatMsg():
    
    num='+212607649781'
    now = datetime.datetime.now()
    h =now.hour
    m =int(now.minute)+1
    try:
        import pywhatkit
        if (old_time != time_list):
            pywhatkit.sendwhatmsg(num,"check your facebook",h,m)
        else:
            pywhatkit.sendwhatmsg(num,"check your code",h,m)
    except:
        import pywhatkit
        if (old_time != time_list):
            pywhatkit.sendwhatmsg(num,"check your facebook",h,m)
        else:
            pywhatkit.sendwhatmsg(num,"check your code",h,m)
    

def run():
    get_page_fb()
    # login_fb()
    # git_post()
    whatMsg()
    if old_time != time_list:
        call_phone()
    
while True:
    run()
