from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class NamedRoadSupplementaryCityName(DarBaseModel):
    named_road: Optional[str] = Field(
        None,
        alias="navngivenVej",
        description="EAID_7CF789EC_31C0_4af3_B75B_77674A26DECD",
    )
    supplementary_city_name: Optional[str] = Field(
        None,
        alias="supplerendeBynavn",
        description="EAID_21C0B8C7_8B67_406c_BDC1_21ADBA284867",
    )
