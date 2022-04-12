import json
from rimzona_cards_class import *
from parse_links import parse_links
import sys
sys.setrecursionlimit(10000)



def record_cards_file(path_to_links_file, parse_func, output_filename, verbose=False):
    """
    takes the path to a file containing an array of BeautifulSoup objects,
    the function of processing the product card page,
    the name of the output file.
    After passing the link, writes the result (json line of object)
    to the file {ozon/rimzona/cards_data/{output_filename}.jsonl}
    and returns True.
    If an error occurs, returns False
    """

    links_array = parse_links(path=path_to_links_file)
    len_links_array = len(links_array)
    record_count = 0
    err_count = 0
    err_links = []
    
    # Verbose mod
    if verbose:

        try:
            
            link_count =0

            with open(output_filename, 'w') as output:
                
                for link in links_array:

                    link_count += 1
                    
                    print('\n<------------->')
                    print(f'\nlink {link_count} from {len_links_array}')
                    
                    card = parse_func(link)

                    if card:
                        jsonStr = json.dumps(card.__dict__, 
                            sort_keys=False,
                            ensure_ascii=False,
                            separators=(',', ': '))
                        output.write(jsonStr)
                        output.write('\n')
                        record_count += 1
                        print(f'\nThe card is recorded')
                        print('\n>>>---------<<<\n\n')
                    else:
                        err_count += 1
                        err_links.append(link)
                        print(f'\nThe card {link_count} was not recorded')
                        print(f'\nlink: {link}')
                        print('\n>>>---------<<<\n\n')


                
                print('\n##########################')
                print(f'\nlen_links_array: {len_links_array}')
                print(f'\nrecord_count: {record_count}')
                if len(err_links) != 0:
                    print('\nerror links:\n')
                    for link in err_links:
                        print(f'\n{link}')
                    print(f'\ntotal error links: {len(err_links)}')
                print('\n')

            return True

        except Exception as ex:
            print('Exception in record_cards_file.py')
            print(ex)
            return False

    # Not verbose mod
    else:

        try:
            
            with open(output_filename, 'w') as output:
                
                for link in links_array:
                    
                    card = parse_func(link)

                    if card:
                        jsonStr = json.dumps(card.__dict__, 
                            sort_keys=False,
                            ensure_ascii=False,
                            separators=(',', ': '))
                        output.write(jsonStr)
                        output.write('\n')
                        record_count += 1
                    else:
                        err_count += 1
                        err_links.append(link)
                
                print('\n##########################')
                print(f'\nlen_links_array: {len_links_array}')
                print(f'\nrecord_count: {record_count}')
                if len(err_links) != 0:
                    print('\nerror links:\n')
                    for link in err_links:
                        print(f'\n{link}')
                    print(f'\ntotal error links: {len(err_links)}')
                print('\n')

            return True
            

        except Exception as ex:
            return False

