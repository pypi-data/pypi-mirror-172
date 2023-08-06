from pathlib import Path
from typing import Iterable, Type

from jsonslicer import JsonSlicer
from pydantic import BaseModel

from dar_etl.schemas.address import Adresse
from dar_etl.schemas.address_point import AddressPoint
from dar_etl.schemas.base_model import DarBaseModel
from dar_etl.schemas.house_number import HouseNumber
from dar_etl.schemas.named_road import NamedRoad
from dar_etl.schemas.named_road_municipal_district import NamedRoadMunicipalDistrict
from dar_etl.schemas.named_road_postal_code import NamedRoadPostalCode
from dar_etl.schemas.named_road_supplementary_city_name import NamedRoadSupplementaryCityName
from dar_etl.schemas.postal_code import PostalCode
from dar_etl.schemas.root_keys import Root
from dar_etl.schemas.supplementary_city_name import SupplementaryCityName


class Metadata(BaseModel):
    root: Root
    dar_model: DarBaseModel
    filename: str


class DarParser:
    _registry: dict[Root, Type[DarBaseModel]] = {
        Root.addresses: Adresse,
        Root.address_points: AddressPoint,
        Root.house_numbers: HouseNumber,
        Root.named_roads: NamedRoad,
        Root.named_road_municipal_parts: NamedRoadMunicipalDistrict,
        Root.named_road_postal_codes: NamedRoadPostalCode,
        Root.named_road_supplementary_city_names: NamedRoadSupplementaryCityName,
        Root.postal_codes: PostalCode,
        Root.supplementary_city_names: SupplementaryCityName,
    }

    def parse(self, filepath: Path) -> Iterable[Metadata]:
        with open(file=filepath, mode="r", encoding="UTF-8") as file_pointer:
            for *key, record in JsonSlicer(
                file=file_pointer,
                path_prefix=(None, None),
                read_size=4096,  # noqa: WPS432
                path_mode="full",
            ):
                root = Root(key[0])
                dar_model = self._registry[root](**record)
                yield Metadata(root=root, dar_model=dar_model, filename=filepath.name)
