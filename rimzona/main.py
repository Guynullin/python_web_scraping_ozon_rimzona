from parse_cards_rimzona import *
from parse_category import parse_category
from rimzona_cards_class import *
from record_cards_file import record_cards_file
from datetime import datetime

url_summer_tire = 'https://rimzona.ru/shiny/letnie/?page='
soup_summer_tire = 'rimzona/page_data/summer_tires_12_04.pkl'
target_summer_tire = 'rimzona/cards_data/summer_tires_12_04.jsonl'

url_winter_tire = 'https://rimzona.ru/shiny/zimnie/?page='
soup_winter_tire = 'rimzona/page_data/winter_tires_12_04.pkl'
target_winter_tire = 'rimzona/cards_data/winter_tires_12_04.jsonl'

url_allseason_tire = 'https://rimzona.ru/shiny/vsesezonnye/?page='
soup_allseason_tire = 'rimzona/page_data/allseason_tires_12_04.pkl'
target_allseason_tire = 'rimzona/cards_data/allseason_tires_12_04.jsonl'

url_alloy_rims = 'https://rimzona.ru/diski/?page='
soup_alloy_rims = 'rimzona/page_data/alloy_rims_12_04.pkl'
target_alloy_rims = 'rimzona/cards_data/alloy_rims_12_04.jsonl'


def main():

    start = datetime.now()

    log = {}

    try:
        if parse_category(
            url=url_summer_tire, 
            start=1, 
            end=100, 
            path=soup_summer_tire):

            if record_cards_file(
                path_to_links_file=soup_summer_tire, 
                parse_func=parse_tire_rimzona, 
                output_filename=target_summer_tire,
                verbose=True):
                log['summer_tires'] = 'success'

        if parse_category(
            url=url_winter_tire, 
            start=1, 
            end=137, 
            path=soup_winter_tire):

            if record_cards_file(
                path_to_links_file=soup_winter_tire, 
                parse_func=parse_tire_rimzona, 
                output_filename=target_winter_tire,
                verbose=True):
                log['winter_tires'] = 'success'

        if parse_category(
            url=url_allseason_tire, 
            start=1, 
            end=20, 
            path=soup_allseason_tire):

            if record_cards_file(
                path_to_links_file=soup_allseason_tire, 
                parse_func=parse_tire_rimzona, 
                output_filename=target_allseason_tire,
                verbose=True):
                log['allseason_tires'] = 'success'

        if parse_category(
            url=url_alloy_rims, 
            start=1, 
            end=133, 
            path=soup_alloy_rims):

            if record_cards_file(
                path_to_links_file=soup_alloy_rims, 
                parse_func=parse_rim_rimzona, 
                output_filename=target_alloy_rims,
                verbose=True):
                log['alloy_rims'] = 'success'

    except Exception as ex:
        print('Exception in main.py')
        print(ex)
    finally:
        end = datetime.now()
        print('\n##################')
        print('\n')
        print(log)
        print('\nEND in main.py')
        print(end - start)

if __name__ == '__main__':
    main()
