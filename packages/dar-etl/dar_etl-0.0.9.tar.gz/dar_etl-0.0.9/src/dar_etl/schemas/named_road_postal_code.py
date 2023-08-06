from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class NamedRoadPostalCode(DarBaseModel):
    named_road: Optional[str] = Field(
        None,
        alias="navngivenVej",
        description="EAID_1B3CAEB0_80FA_486f_ABD1_818B332C905C",
    )
    postal_code: Optional[str] = Field(
        None,
        alias="postnummer",
        description="EAID_AD2844E3_7F05_4d8d_967E_44BA3D12C4B4",
    )
