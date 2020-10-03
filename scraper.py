from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def tesT():
  #Path to chromedriver
  chromedriver_path = r'/home/mikael/Documents/Projects/sky_scraper/chromedriver'

  #create an instance with Options, add --headless webpage
  chrome_options = Options()
  #chrome_options.add_argument('--headless')

  #add the options instance to the webdriver/browser
  driver = webdriver.Chrome(
    executable_path=chromedriver_path, options=chrome_options
  )

  driver.get('https://authoraditiagarwal.com/leadershipmanagement')

  scrape_result = driver.find_element_by_xpath('/html/body').get_attribute('outerHTML')


  print(scrape_result)


if __name__ == '__main__':
    tesT()
