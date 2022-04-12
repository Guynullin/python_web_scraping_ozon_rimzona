from dataclasses import dataclass

@dataclass
class Card:
    """
    describes the product card, 
    compatible with the product cards of the ozon website
    """
    title: str = False
    price: str = False
    brand: str = False
    model: str = False
    partnum: str = False
    sku: str = False
    category: str = False
    desc: str = False
    src1: str = False
    src2: str = False
    car_brand: str = False
    car_model: str = False
    material: str = False
    complect: str = False
    color: str = False
    country: str = False
    link: str = False
        
