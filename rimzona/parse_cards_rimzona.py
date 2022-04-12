from bs4 import BeautifulSoup
import re
import time
import requests
from rimzona_cards_class import *


def parse_tire_rimzona(link):
    """
    takes the url of the product card page and returns the Tire(Card) object
    if an error occurs, returns False
    """
    flag = True
    err_count = 0

    while flag:

        try:
            r = requests.get(link)

            soup = BeautifulSoup(r.text, 'lxml')

            if soup.find('div', class_='product-data'):
                product_data = soup.find('div', class_='product-data')
            else: return False
            
            if product_data.find('h1', {'itemprop' : 'name'}):
                title = product_data.find('h1', {'itemprop' : 'name'}).text
            else: title = False

            if product_data.find('img', {'src' : True}):
                main_img = product_data.find('img', {'src' : True})
                src1 = main_img.get('src')
                src1 = f'https://rimzona.ru{src1}'
            else: src1 = False

            if product_data.find('img', {'data-src' : True}):
                first_min_img = product_data.find('img', {'data-src' : True})
                if first_min_img.find_next_sibling('img', {'data-src' : True}):
                    second_min_img = first_min_img.find_next_sibling('img', {'data-src' : True})
                    src2 = second_min_img.get('data-src')
                    src2 = f'https://rimzona.ru{src2}'
                else: src2 = False
            else: src2 = False
            
            if product_data.find('meta', {'itemprop' : 'price', 'content' : True}):
                price = product_data.find('meta', {'itemprop' : 'price', 'content' : True}).get('content')
                # price = ''.join(re.findall(r'\d+', price))
            else: price = False

            if product_data.find('ul'):
                ul = product_data.find('ul')

                # Диаметр
                if ul.find("span", string=re.compile("Диаметр*")):
                    size = ul.find("span", string=re.compile("Диаметр*")).next_sibling.next_sibling
                    if size:
                        size = size.string
                    else: size = False
                else: size = False

                # Ширина
                if ul.find("span", string=re.compile("Ширина*")):
                    width = ul.find("span", string=re.compile("Ширина*")).next_sibling.next_sibling
                    if width:
                        width = width.string
                    else: width = False
                else: width = False

                # Высота
                if ul.find("span", string=re.compile("Высота*")):
                    aspect_ratio = ul.find("span", string=re.compile("Высота*")).next_sibling.next_sibling
                    if aspect_ratio:
                        aspect_ratio = aspect_ratio.string
                    else: aspect_ratio = False
                else: aspect_ratio = False

                # Сезонность
                if ul.find("span", string=re.compile("Сезонность*")):
                    season = ul.find("span", string=re.compile("Сезонность*")).next_sibling.next_sibling
                    if season:
                        season = season.string
                    else: season = False
                else: season = False

                # Шипы
                if ul.find("span", string=re.compile("Шипы*")):
                    studdable = ul.find("span", string=re.compile("Шипы*")).next_sibling.next_sibling
                    if studdable:
                        studdable = studdable.string
                    else: studdable = False
                else: studdable = False

                # Индекс нагрузки
                if ul.find("span", string=re.compile("Индекс нагрузки*")):
                    load_index = ul.find("span", string=re.compile("Индекс нагрузки*")).next_sibling.next_sibling
                    if load_index:
                        load_index = load_index.string
                    else: load_index = False
                else: load_index = False

                # Индекс скорости
                if ul.find("span", string=re.compile("Индекс скорости*")):
                    speed_rating = ul.find("span", string=re.compile("Индекс скорости*")).next_sibling.next_sibling
                    if speed_rating:
                        speed_rating = speed_rating.string
                    else: speed_rating = False
                else: speed_rating = False

                # Производитель
                if ul.find("span", string=re.compile("Производитель*")):
                    brand = ul.find("span", string=re.compile("Производитель*")).next_sibling.next_sibling
                    if brand:
                        brand = brand.string
                    else: brand = False
                else: brand = False

                # Модель
                if ul.find("span", string=re.compile("Модель*")):
                    model = ul.find("span", string=re.compile("Модель*")).next_sibling.next_sibling
                    if model:
                        model = model.string
                    else: model = False
                else: model = False
            else: size, width, aspect_ratio, season, studdable, load_index, speed_rating, brand, model = False

            tire = Tire(title=title, price=price, brand=brand, model=model, category='tire', src1=src1, src2=src2, complect='1шт.', link=link, width=width, aspect_ratio=aspect_ratio, size=size, season=season, studdable=studdable, load_index=load_index, speed_rating=speed_rating)
            
            flag = False

            return tire

        except Exception as ex:
            print(f'\n{ex}')
            err_count += 1
            time.sleep(2)
            if err_count >= 5:
                flag = False
                return False
        
    return False


def parse_rim_rimzona(link):
    """
    takes the url of the product card page and returns the Rim(Card) object
    if an error occurs, returns False
    """
    flag = True
    err_count = 0

    while flag:

        try:
            r = requests.get(link)

            soup = BeautifulSoup(r.text, 'lxml')

            if soup.find('div', class_='product-data'):
                product_data = soup.find('div', class_='product-data')
            else: return False
            
            if product_data.find('h1', {'itemprop' : 'name'}):
                title = product_data.find('h1', {'itemprop' : 'name'}).text
            else: title = False

            if product_data.find('img', {'src' : True}):
                main_img = product_data.find('img', {'src' : True})
                src1 = main_img.get('src')
                src1 = f'https://rimzona.ru{src1}'
            else: src1 = False

            if product_data.find('img', {'data-src' : True}):
                first_min_img = product_data.find('img', {'data-src' : True})
                if first_min_img.find_next_sibling('img', {'data-src' : True}):
                    second_min_img = first_min_img.find_next_sibling('img', {'data-src' : True})
                    src2 = second_min_img.get('data-src')
                    src2 = f'https://rimzona.ru{src2}'
                else: src2 = False
            else: src2 = False
            
            if product_data.find('meta', {'itemprop' : 'price', 'content' : True}):
                price = product_data.find('meta', {'itemprop' : 'price', 'content' : True}).get('content')
                # price = ''.join(re.findall(r'\d+', price))
            else: price = False

            if product_data.find('ul'):
                ul = product_data.find('ul')

                # Диаметр
                if ul.find("span", string=re.compile("Диаметр*")):
                    size = ul.find("span", string=re.compile("Диаметр*")).next_sibling.next_sibling
                    if size:
                        size = size.string
                    else: size = False
                else: size = False

                # Ширина
                if ul.find("span", string=re.compile("Ширина*")):
                    width = ul.find("span", string=re.compile("Ширина*")).next_sibling.next_sibling
                    if width:
                        width = width.string
                    else: width = False
                else: width = False

                # Диаметр центрального отверстия
                if ul.find("span", string=re.compile("Диаметр ц*")):
                    dia = ul.find("span", string=re.compile("Диаметр ц*")).next_sibling.next_sibling
                    if dia:
                        dia = dia.string
                    else: dia = False
                else: dia = False

                # Сверловка PCD
                if ul.find("span", string=re.compile("Сверловка*")):
                    pcd = ul.find("span", string=re.compile("Сверловка*")).next_sibling.next_sibling
                    if pcd:
                        pcd = pcd.string
                    else: pcd = False
                else: pcd = False

                # Вылет ET
                if ul.find("span", string=re.compile("Вылет*")):
                    et = ul.find("span", string=re.compile("Вылет*")).next_sibling.next_sibling
                    if et:
                        et = et.string
                    else: et = False
                else: et = False

                # Тип
                if ul.find("span", string=re.compile("Тип*")):
                    type_disk = ul.find("span", string=re.compile("Тип*")).next_sibling.next_sibling
                    if type_disk:
                        type_disk = type_disk.string
                    else: type_disk = False
                else: type_disk = False

                # Цвет
                if ul.find("span", string=re.compile("Цвет*")):
                    color = ul.find("span", string=re.compile("Цвет*")).next_sibling.next_sibling
                    if color:
                        color = color.string
                    else: color = False
                else: color = False

                # Производитель
                if ul.find("span", string=re.compile("Производитель*")):
                    brand = ul.find("span", string=re.compile("Производитель*")).next_sibling.next_sibling
                    if brand:
                        brand = brand.string
                    else: brand = False
                else: brand = False

                # Модель
                if ul.find("span", string=re.compile("Модель*")):
                    model = ul.find("span", string=re.compile("Модель*")).next_sibling.next_sibling
                    if model:
                        model = model.string
                    else: model = False
                else: model = False
            else: size, width, dia, pcd, et, type_disk, color, brand, model = False

            rim = Rim(title=title, price=price, brand=brand, model=model, category='rim', src1=src1, src2=src2, complect='1шт.', link=link, width=width, color=color, size=size, dia=dia, pcd=pcd, et=et, type_disk=type_disk)

            return rim

        except Exception as ex:
            print(f'\n{ex}')
            err_count += 1
            time.sleep(2)
            if err_count >= 5:
                flag = False
                return False
        
    return False