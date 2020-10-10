from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
import time
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from email_smtp import smtp_mail

max_flight_price = 6200
max_flight_time = 21

#Create a headless firefox driver
#TODO fix the relative path
def create_driver():

  options = Options()
  options.add_argument("--headless")
  driver = webdriver.Firefox(executable_path='/home/mikael/Documents/Projects/sky_scraper/geckodriver', options=options)


  return driver


def scrape(driver):

  #url to scrape
  #https://www.momondo.se/flight-search/LLA-BKK/2021-06-08/2021-07-24?sort=price_a, attention this is suited for momondo
  url = "https://www.momondo.se/flight-search/"
  depature = "LLA-"
  arrival = "BKK/"
  depatureMonthNumber = 6
  depatureDayNumber = 8
  gobackMonthNumber = 7
  gobackDayNumber = 24
  depature_date = "2021-06-08"
  goback_month = "2021-07-24"
  sort = "?sort=price_a"
  
  #loop depature date and arrival date
  k = 0
  try:
    while(k < 3):
      
      l = 0
      while(l < 3):
        #scrape this page
        driver.get(url+depature+arrival+depature_date+"/"+goback_month+sort)
        print(url+depature+arrival+depature_date+"/"+goback_month+sort)
        time.sleep(10)
        element = driver.find_element_by_xpath("//div[contains(@class, 'tabGrid')]")

        element_list = element.text.split("\n")
        print(element_list)
        i = 0
        result_list = []
        while(i < 6):
          price_and_time = element_list[i+1]
          price = price_and_time[:8]
          price = re.sub('\D', '', price)
          price = price.replace(" ", "")

          flight_time = price_and_time[9:12]
          flight_time = re.sub('\D', '', flight_time)
          flight_time = flight_time.replace(" ", "")

          result_list.extend(([element_list[i], flight_time, price]))
          i += 2

        #check the result
        i = 0
        best_price = 0
        best_time = 0
        trip_founded = False
        message = ""
        while(i < 9):
          if(max_flight_time > int(result_list[i+1]) and max_flight_price > int(result_list[i+2])):
            best_price = int(result_list[i+2])
            best_time = int(result_list[i+1])
            #todo create an email with proper content
            print("email cheapest")
            message = result_list[i]+" time: "+result_list[i+1]+" hours  price: "+result_list[i+2]+" depature: "+depature_date+" go back at: "+goback_month
            trip_founded = True
          if(result_list[i] != "Billigaste"):
            if(best_price+1000 > int(result_list[i+2]) and best_time-4 > int(result_list[i+1])):
              message = result_list[i]+" time: "+result_list[i+1]+" hours  price: "+result_list[i+2]+" depature: "+depature_date+" go back at: "+goback_month
              trip_founded = True
              print("email recommended/fastest")
          if(trip_founded):
            return message
          i += 3

        l += 1
        gobackDayNumber += 1
        goback_month = increase_goback_date(gobackMonthNumber, gobackDayNumber)

      k += 1
      depatureDayNumber += 1
      depature_date = increase_depature_date(depatureMonthNumber, depatureDayNumber)
      #set gobackDayNumber - 3, since we have loop one round now
      gobackDayNumber -= 3
      return ""

  except:
    print("An exception occurred") 

def increase_depature_date(depatureMonthNumber, depatureDayNumber):
  date_increased = datetime.now()+ relativedelta(years = 1, month = depatureMonthNumber, day = depatureDayNumber)
  return str(date_increased.strftime('%Y/%m/%d')).replace("/", "-")

def increase_goback_date(gobackMonthNumber, gobackDayNumber):
  date_increased = datetime.now()+ relativedelta(years = 1, month = gobackMonthNumber, day = gobackDayNumber)
  return str(date_increased.strftime('%Y/%m/%d')).replace("/", "-")


if __name__ == '__main__':
    webdriver = create_driver()
    text = scrape(webdriver)
    webdriver.quit()
    if(len(text) > 0):
      sender = 'sender@fromdomain.com'
      receiver = ['reciever@todomain.com']  
      mess = """From: From Person %s  
    To: To Person %s  
    
    %s
    """%(sender,receiver, text)
      smtp_mail.send(sender, receiver, mess)
