import pickle
from bs4 import BeautifulSoup
import sys
sys.setrecursionlimit(10000)



def parse_links(path):
    """
    takes the path to a file containing div blocks
    with links to product cards. 
    return array(str) which every element is a link 
    """
    
    soup_array = []
    links_array = []

    with open(path, 'rb') as file:
        soup_array = pickle.load(file)

    try:
        for doc in soup_array:
            div_catalog_prod_wrap = BeautifulSoup(doc, 'lxml')
            div_array = div_catalog_prod_wrap.find_all('div', class_='col mb-3 px-2')
            for div in div_array:
                href = div.find('a', href=True).get('href')
                link = f'https://rimzona.ru{href}'
                links_array.append(link)
        
        return links_array
        
    except Exception as ex:
        print('<----------!---------->')
        print('Exception in parse_links.py\n\n\n')
        print(ex)
        return False
