from enum import Enum


class Root(Enum):
    addresses = "AdresseList"
    address_points = "AdressepunktList"
    house_numbers = "HusnummerList"
    named_roads = "NavngivenVejList"
    named_road_municipal_parts = "NavngivenVejKommunedelList"
    named_road_postal_codes = "NavngivenVejPostnummerList"
    named_road_supplementary_city_names = "NavngivenVejSupplerendeBynavnList"
    postal_codes = "PostnummerList"
    supplementary_city_names = "SupplerendeBynavnList"
