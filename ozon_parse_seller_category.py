from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import pickle
import time
import random

def ozon_parse_seller_category(url, file_name):
    """
    The function creates an array {soup_array} where each element is
    a str(Beautiful Soup object) of seller's category page.
    At the end writes the result to a file {file_name}
    and returns True.
    
    And creates a log file {parse_seller_category_error_log.txt}
    in the current directory with parsing errors.

    The function will return False if it cannot write the file,
    otherwise it will return True.

    :Args:
     url: URL of the first page of the product category
    {example: https://www.ozon.ru/seller/rz-accessories-127693/products/?miniapp=seller_127693}
     file_name: the path to the file where the result will be recorded 
    (a list of the str(BeautifulSoup objects)).
    """

    # Pages
    soup_array = []
    page_count = 1

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
    driver.set_page_load_timeout(20)


    with open('parse_seller_category_error_log.txt', 'w') as log:
        log.write(f'\n<-----------{time.ctime()}----------->\n\n')

    print('webdriver created')

    try:

        # Open page
        driver.get(url=url)
        time.sleep(random.randrange(1, 3))

        print(f'page #{page_count} opened')

        # Scroll down
        html = driver.find_element(By.TAG_NAME, 'html')
        for i in range(13):
            html.send_keys(Keys.PAGE_DOWN)
            print('scroll..')
        time.sleep(1)
        
        print(f'page #{page_count} scrolled down')


        # Create Beautiful Soup object
        soup = BeautifulSoup(driver.page_source, 'lxml')
        print(f'soup #{page_count} created')
        
        soup_array.append(str(soup))
        print(f'soup added to array')
        print('<-------------------->\n\n')

        button_exists = driver.find_elements(By.LINK_TEXT, 'Дальше')

        
        while button_exists:

            page_count += 1
            
            next_button_url = driver.find_element(By.LINK_TEXT, 'Дальше').get_attribute('href')

            driver.get(next_button_url)

            time.sleep(random.randrange(1, 3))

        
            print(f'page #{page_count} opened')

            # Scroll down
            html = driver.find_element(By.TAG_NAME, 'html')
            for i in range(13):
                html.send_keys(Keys.PAGE_DOWN)
                print('scroll..')
            time.sleep(1)
            print(f'page #{page_count} scrolled down')

            # Create Beautiful Soup object
            soup = BeautifulSoup(driver.page_source, 'lxml')
            print(f'soup #{page_count} created')
            
            soup_array.append(str(soup))
            print(f'soup added to array')
            print('<-------------------->\n\n')

            button_exists = driver.find_elements(By.LINK_TEXT, 'Дальше')

        print('end parsing')
        print(f'len soup_array: {len(soup_array)}')

        


    except Exception as ex:
        driver.close()
        driver.quit()
        with open('parse_seller_category_error_log.txt', 'a') as log:
                    log.write(time.ctime())
                    log.write(f'\n{str(ex)}')
                    log.write(f'\nurl: {url}')
                    log.write('\n<-------->\n')

    finally:
        with open('parse_seller_category_error_log.txt', 'a') as log:
            log.write(f'\n\n<-----------END----------->\n')
            log.write(f'<-----------{time.ctime()}----------->\n')
        driver.close()
        driver.quit()

    if len(soup_array) > 0:
        with open(file_name, 'wb') as file:
                pickle.dump(soup_array, file)

        print(f'{file_name} recorded')

        return True
    
    else: return False
