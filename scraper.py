from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

max_flight_price = 6200
max_flight_time = 21

def create_driver():
  #Path to chromedriver
  chromedriver_path = r'/home/mikael/Documents/Projects/sky_scraper/chromedriver'

  #create an instance with Options, add --headless webpage
  chrome_options = Options()
  #chrome_options.add_argument('--headless')

  #add the options instance to the webdriver/browser
  driver = webdriver.Chrome(
    executable_path=chromedriver_path, options=chrome_options
  )


  return driver


def scrape(driver):

  #url to scrape
  #https://www.momondo.se/flight-search/LLA-BKK/2021-06-08/2021-07-24?sort=price_a, attention this is suited for momondo
  url = "https://www.momondo.se/flight-search/"
  depature = "LLA-"
  arrival = "BKK/"
  depature_date = "2021-06-08"
  arrival_date = "2021-07-24"
  sort = "?sort=price_a"
  
  #loop depature date and arrival date
  k = 0
  while(k < 3):
    
    l = 0
    arrival_date = "2021-07-24"
    while(l < 3):
      #scrape this page
      driver.get(url+depature+arrival+depature_date+"/"+arrival_date+sort)
      print(url+depature+arrival+depature_date+"/"+arrival_date+sort)
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
      while(i < 9):
        if(max_flight_time > int(result_list[i+1]) and max_flight_price > int(result_list[i+2])):
          best_price = int(result_list[i+2])
          best_time = int(result_list[i+1])
          #todo create an email with proper content
          print("email cheapest")
          print(result_list[i]+" time: "+result_list[i+1]+" price: "+result_list[i+2]+" depature: "+depature_date+" arrival: "+arrival_date)
        if(result_list[i] != "Billigaste"):
          if(best_price+1000 > int(result_list[i+2]) and best_time-4 > int(result_list[i+1])):
            print("email recommended/fastest")
        i += 3
      #change arrival_date
      if(int(arrival_date[-2:]) > 10):
        arrival_date = arrival_date[:-2]+str((int(arrival_date[-2:])+1))
      else:
        arrival_date = arrival_date[:-2]+"0"+str((int(arrival_date[-2:])+1))
      l += 1
    
    #change depature_date
    if(int(depature_date[-2:]) > 10):
      depature_date = depature_date[:-2]+str((int(depature_date[-2:])+1))
    else:
      depature_date = depature_date[:-2]+"0"+str((int(depature_date[-2:])+1))

    k += 1


if __name__ == '__main__':
    webdriver = create_driver()
    scrape(webdriver)

