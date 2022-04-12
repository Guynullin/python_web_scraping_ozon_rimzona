import string
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import json
import re
from card_class import Card

def parse_card(document, link):
    """
    Extracts information from a BeautirulSoup object and creates the Card object
    and returns it.
     :Args:
     document: the page {str(html)} of the product card.
     link: url of the page
    
    If an error occurs, returns False.
    """

    # Create Beautiful Soup object
    soup = BeautifulSoup(document, 'lxml')
    print('soup created')

    try:
        # If the product is over
        if soup.find('div', {'data-widget' : 'webPrice'}).div.text == 'Товар закончился':
            print('<------------>\n\n')
            return False
        
        # Find title
        if soup.find('div', {'data-widget' : 'webProductHeading'}):
            title = soup.find('div', {'data-widget' : 'webProductHeading'}).text
        else: 
            print('<------------>\n\n')
            return False

        # Find price
        if soup.find('div', {'data-widget' : 'webPrice'}).div.div:

            dirty_price = soup.find('div', {'data-widget' : 'webPrice'}).div.div.find_next_sibling('div')
            
            if dirty_price:
                dirty_price = dirty_price.text
                price_list  = dirty_price.split('₽')
                price = []
                
                for item in price_list:
                    
                    digit_list = re.findall('\d', item)
                    out_str = ''.join(digit_list)
                    
                    if out_str.isdigit():
                        price.append(out_str)
            else: price = False
        else: 
            price = False

        # If the price is not found - start searching in another block
        if price == False:
            if soup.find('div', {'id' : re.compile('state-webPrice*')}):
                state_webPrice = soup.find('div', {'id' : re.compile('state-webPrice*')}).get('data-state').replace(u"\u2009", " ")

                data_state = json.loads(state_webPrice)

                price = []
                price.append(data_state['price'].replace(" ₽", ""))
                price.append(data_state['originalPrice'].replace(" ₽", ""))

        # 
        # Search for product characteristics
        # 
        if soup.find('div', {'data-widget' : 'webCharacteristics'}):
            webCharacteristics = soup.find('div', {'data-widget' : 'webCharacteristics'})
            
            if webCharacteristics.find('span', string=re.compile("Бренд*")):
                brand = webCharacteristics.find('span', string=re.compile("Бренд*")).parent.next_sibling.text
            else: brand = False
            
            if webCharacteristics.find('span', string=re.compile("Партномер*")):
                partnum = webCharacteristics.find('span', string=re.compile("Партномер*")).parent.next_sibling.text
            else: partnum = False
            
            if webCharacteristics.find('span', string=re.compile("Артикул*")):
                sku = webCharacteristics.find('span', string=re.compile("Артикул*")).parent.next_sibling.text
            else: sku = False
            
            if webCharacteristics.find('span', string=re.compile("Тип*")):
                category = webCharacteristics.find('span', string=re.compile("Тип*")).parent.next_sibling.text
            else: category = False
            
            if webCharacteristics.find('span', string=re.compile("Марка*")):
                car_brand = webCharacteristics.find('span', string=re.compile("Марка*")).parent.next_sibling.text
            else: car_brand = False
        else: 
            brand = False
            partnum = False
            sku = False
            category = False
            car_brand = False


        if soup.find('h2', string='Описание'):
            desc = soup.find('h2', string='Описание').next_sibling.next_sibling.text
        else: desc = False

        if soup.find('div', {'data-widget' : 'webGallery'}):
            img = soup.find('div', {'data-widget' : 'webGallery'}).img
            src1 = img.get('src')
            if src1:
                src2 = src1.replace('wc1200', 'wc250')
            else: src2 = False
        else:
            src1 = False
            src2 = False

        if soup.find('div', id='section-characteristics'):
            section_characteristics = soup.find('div', id='section-characteristics')
            
            if section_characteristics.find('span', string=re.compile('Модель*')):
                car_model = section_characteristics.find('span', string=re.compile('Модель*')).parent.next_sibling.text
            else: car_model = False
            
            if section_characteristics.find('span', string=re.compile('Материал*')):
                material = soup.find('span', string=re.compile('Материал*')).parent.next_sibling.text
            else: material = False
            
            if section_characteristics.find('span', string='Цвет'):
                color = section_characteristics.find('span', string='Цвет').parent.next_sibling.text
            else: color = False
            
            if section_characteristics.find('span', string='Страна-изготовитель'):
                country = section_characteristics.find('span', string='Страна-изготовитель').parent.next_sibling.text
            else: country = False
        else:
            car_model = False
            material = False
            color = False
            country = False
        
        if soup.find('h3', string='Комплектация'):
            complect = soup.find('h3', string='Комплектация').next_sibling.text
        elif soup.find('div', id='section-characteristics'):
            section_characteristics = soup.find('div', id='section-characteristics')
            if section_characteristics.find('span', string='Количество, штук'):
                complect = section_characteristics.find('span', string='Количество, штук').parent.next_sibling.text
            else: complect = False
        elif soup.find('div', id='section-characteristics'):
            section_characteristics = soup.find('div', id='section-characteristics')
            if section_characteristics.find('span', string=re.compile('Количество в упа*')):
                complect = section_characteristics.find('span', string='Количество, штук').parent.next_sibling.text
            else: complect = False
        else: complect = False
        
        model = False

        card = Card(title=title, price=price, brand=brand, model=model, partnum=partnum, sku=sku, category=category, desc=desc, src1=src1, src2=src2, car_brand=car_brand, car_model=car_model, material=material, complect=complect, color=color, country=country, link=link)

        return card
    
    except Exception as ex:
        print(ex)
        return False