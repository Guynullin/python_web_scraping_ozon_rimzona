from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import pickle
import time
import random


def parse_category(url, start, end, path):
    """ takes the url{example: https://rimzona.ru/shiny/letnie/?page=}
    of the product category and
    the indexes of the first and last page.
    The function creates an array {page_array} where each element is
    a div-block of goods.
    At the end writes the result to a file {path}
    and returns True
    """

    page_array = []

    # Create webdriver options
    options = webdriver.FirefoxOptions()

    # headless
    options.headless = True

    # add user-agent
    # options.set_preference('general.useragent.override','user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')

    # disable webdriver-mode
    options.set_preference('dom.webdriver.enabled', False)
    options.set_preference('useAutomationExtension', False)

    # Create webdriver and add options
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    # Timeout 
    driver.set_page_load_timeout(10)


    print('webdriver created')
    page_count = 0

    for i in range(start, end + 1):

        page_count += 1
        flag = True
        err_count = 0

        print(f'\n{i}')
        page_link = f'{url}{str(i)}'
        print(page_link)

        while flag:
            
            try:
                
                # Open page
                driver.get(url=page_link)

                # time.sleep(random.randrange(1, 2))

                # Scroll down
                html = driver.find_element(By.TAG_NAME, 'html')
                for i in range(7):
                    html.send_keys(Keys.PAGE_DOWN)
                print('the page is scrolled down')

                if len(driver.find_elements(By.XPATH, "//div[contains(text(), 'Страница не найдена')]")) == 0:
                    
                    if len(driver.find_elements(By.ID, 'catalog-prod-wrap')) != 0:

                        div_catalog = driver.find_element(By.ID, 'catalog-prod-wrap').get_attribute("innerHTML")

                        soup = BeautifulSoup(div_catalog, 'lxml')

                        page_array.append(str(soup))

                        print('Page is added to page_array')

                        flag = False

                else: 
                    print('Page not found!')
                    err_count += 1
                    if err_count >= 3:
                        print(f'page {i} was not added to array')
                        print('\n===========\n')
                        flag = False
            
            except Exception as ex:
                err_count += 1
                print(ex)
                print('\nretry..\n')
                if err_count >= 5:
                    print(f'page {i} was not added to array')
                    print('\n===========\n')
                    flag = False

    with open(path, 'wb') as file:
        pickle.dump(page_array, file)
        print('\n#########################')
        print('\nThe file is recorded')
        print(f'\n{page_count} pages completed')
        print(f'\n{len(page_array)} pages added to the array')
        
    
    driver.close()
    driver.quit()

    time.sleep(2)

    return True