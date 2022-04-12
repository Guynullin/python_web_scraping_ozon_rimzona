from ozon_parse_seller_category import ozon_parse_seller_category
from ozon_parse_cards import ozon_parse_cards


def main():
    soup_file_name = 'ozon_category_data/rimzona_all_cards_soup.pkl'
    try:
        if ozon_parse_seller_category(
            url='https://www.ozon.ru/seller/rz-accessories-127693/products/?miniapp=seller_127693', 
            file_name=soup_file_name):
            ozon_parse_cards(
                path=soup_file_name, 
                file_name='ozon_pages_data/rimzona_all_cards.jsonl')

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()

