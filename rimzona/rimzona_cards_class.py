from dataclasses import dataclass
import sys
sys.path.append('./')
from card_class import Card

@dataclass
class Tire(Card):
    # Ширина
    width: str = False
    # Высота профиля
    aspect_ratio: str = False
    # Размер/Диаметр диска
    size: str = False
    # Сезонность
    season: str = False
    # Шипы
    studdable: bool = False
    # Ran Flat
    ran_flat: str = False
    # Индекс нагрузки (95, 98, 100)
    load_index: str = False
    # Индекс скорости (J - Z/ZR; min - max)
    speed_rating: str = False


@dataclass
class Rim(Card):
    # Размер/Диаметр
    size: str = False
    # Ширина диска
    width: str = False
    # Диаметр центрального отверстия
    dia: str = False
    # Сверловка
    pcd: str = False
    # Вылет
    et: str = False
    # Тип (штамп, литые, ковка)
    type_disk: str = False


