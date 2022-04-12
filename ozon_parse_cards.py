from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from get_links import get_links
from datetime import datetime
import time
import json
from parse_card import *
from card_class import *


def ozon_parse_cards(path, file_name):

    """
    Opens product card pages and writes the information
    (Card objects) to a jsonl file.
    
    And creates a log file {parse_cards_error_log.txt}
    in the current directory with parsing errors.

    :Args:
     path: The path to a file containing a list of the BeautifulSoup objects
    with links that lead to product cards.
     file_name: The path to a jsonl file with the result (the json line of the Card object).
    
    At the end returns True.
    """

    start_time = datetime.now()

    # Prepare links from list of BeautifulSoup objects
    links_array = get_links(path=path)
    len_links_array = len(links_array)
    print('\n===================')
    print('links_array created')
    print('===================\n')


    # Create error log file
    with open('parse_cards_error_log.txt', 'w') as log:
        log.write(f'\n<-----------{str(datetime.now())}----------->\n\n')
        print('jsonl file created\n')

    # Create jsonl file
    with open(file_name, 'w') as output:
        print(f'{file_name} file created\n')

    page_count = 0
    jsonl_count = 0
    err_delay = 3

    # Create webdriver options
    options = webdriver.FirefoxOptions()

    # headless
    options.headless = True

    # add user-agent
    options.set_preference('general.useragent.override','user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')

    # disable webdriver-mode
    options.set_preference('dom.webdriver.enabled', False)
    options.set_preference('useAutomationExtension', False)

    # Create webdriver and add options
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)

    # Timeout 
    driver.set_page_load_timeout(10)

    
    for link in links_array:
    
        page_count += 1

        # Add json line to the file
        with open(file_name, 'a') as output:

            flag = True
            err_count = 0

            print(f'\n <--------------START PAGE {page_count}-------------->\n')

            while flag:

                try:
                    # Open page
                    driver.get(url=link)
                    
                    print(f'page {page_count} from {len_links_array} opened')
                    print(f'\nlink: {link}\n')
                    

                    # Scroll page
                    html = driver.find_element(By.TAG_NAME, 'html')
                    if err_count == 0:
                        time.sleep(0.5)
                        # Fast scroll down
                        for i in range(7):
                            html.send_keys(Keys.PAGE_DOWN)
                            print('fast scrolling..')
                    else:
                        time.sleep(2)
                        # Slow scroll down
                        for i in range(7):
                            time.sleep(0.7)
                            html.send_keys(Keys.PAGE_DOWN)
                            print('slow scrolling..')
                        
                    # Get Card object
                    card = parse_card(driver.page_source, link)

                    if card:
                        
                        if card.title == False or card.price == False:
                            raise ValueError("\ndescription or price not found\n")
                        
                        print(f'\n{card}')
                        print(f'\nlink: {link}')
                        print(f'\n >>>>>>>>>>>>>>>END PAGE {page_count}<<<<<<<<<<<<<<<\n')
                        
                        # Record a line
                        jsonStr = json.dumps(card.__dict__, 
                            sort_keys=False,
                            ensure_ascii=False,
                            separators=(',', ': '))
                        output.write(jsonStr)
                        output.write('\n')
                        
                        jsonl_count += 1
                        err_count = 0
                        flag = False
                    else:
                        raise ValueError("\nCard object is False\n")
                    
                except Exception as ex:
                    
                    flag = True
                    err_count += 1
                    
                    print(f'Error: {ex}\n')
                    print(f'link: {link}\n')
                    print(f'err_count: {err_count}')
                    print('\nretry..\n')

                    with open('parse_cards_error_log.txt', 'a') as log:
                        log.write('\n<-------->\n')
                        log.write(str(datetime.now()))
                        log.write(f'\n{str(ex)}')
                        log.write(f'\nlink: {link}')
                        log.write(f'\n\nerr_count: {err_count}')
                        log.write(f'\npage: {page_count}')
                        log.write('\n<-------->\n\n')
                    
                    time.sleep(err_delay)
                    
                
                if err_count >= 5:
                    
                    flag = False
                    
                    print(f'Attention, the page {page_count} was not added to the file. \n')
                    print(f'link: {link}\n')
                    print(f'err_count: {err_count}')


                    time.sleep(err_delay)
                    with open('parse_cards_error_log.txt', 'a') as log:
                        log.write('\n============================================================================')
                        log.write('\n============================================================================\n')
                        log.write(str(datetime.now()))
                        log.write(f'\nAttention, the page {page_count} was not added to the file.')
                        log.write(f'\nlink: {link}')
                        log.write(f'\n\nerr_count: {err_count}')
                        log.write(f'\npage: {page_count}')
                        log.write('\n============================================================================')
                        log.write('\n============================================================================\n\n\n\n')
                    
                    time.sleep(err_delay)
                
            

    with open('parse_cards_error_log.txt', 'a') as log:
        log.write(f'\n\n\n##############################################')
        log.write(f'\nnumber of links: {len_links_array}')
        log.write(f'\nnumber of pages: {page_count}')
        log.write(f'\nnumber of recorded lines: {jsonl_count}')
        log.write(f'\n<-----------END----------->')
        log.write(f'\n>>>---------{str(datetime.now())}---------<<<')
        log.write(f'\n>>>---------{str(datetime.now() - start_time)}---------<<<\n')
    
    driver.close()
    driver.quit()

    print(f'\n\n\nnumber of links: {len_links_array}')
    print(f'\nnumber of pages: {page_count}')
    print(f'\nnumber of recorded lines: {jsonl_count}')
    print(str(datetime.now() - start_time))
    print('End')

    return True