from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
  
  #scrape this page
  driver.get(url+depature+arrival+depature_date+"/"+arrival_date+sort)
  scrape_result = driver.find_element_by_class_name('resultInner')
  scrape_result_text = scrape_result.get_attribute('outerHTML')

  print(scrape_result_text)
  #print('scrape_result.text: {0}'.format(scrape_result_text))
  #print('scrape_result.get_attribute(\'value\'): {0}'.format(scrape_result_attribute_value))


if __name__ == '__main__':
    webdriver = create_driver()
    scrape(webdriver)

