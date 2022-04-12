import pickle
from bs4 import BeautifulSoup

def get_links(path):
    """
    Extracts links to product cards from the array containg
    the BeautifulSoup objects.

    :Args:
     path: The path to a file containing a list of Beautiful soup objects.

    Returns a list with links (str)
    """

    # Array of differences
    soup_array = []

    # Links array
    links_array = []

    # Array of Apartments objects
    with open(path, 'rb') as file:
        soup_array = pickle.load(file)
        print('file loaded')

    for soup_item in soup_array:

            soup = BeautifulSoup(soup_item, 'lxml')
            container = soup.find('div', {'class' : 'widget-search-result-container'}).find('div')
            div_item = container.find('div')
            
            while div_item:
                
                if div_item.find('a', href=True):
                    
                    href = div_item.find('a', href=True).get('href')
                    link = f'https://ozon.ru{href}'
                    links_array.append(link)

                container.find('div').decompose()
                div_item = container.find('div')
            
    return links_array
