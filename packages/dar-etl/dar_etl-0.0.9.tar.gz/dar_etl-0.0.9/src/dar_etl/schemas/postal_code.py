from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class PostalCode(DarBaseModel):
    name: Optional[str] = Field(
        None,
        alias="navn",
        description="EAID_9E7FA46D_52D9_4615_B24C_599BB28D1923",
    )
    postal_code: Optional[str] = Field(
        None,
        alias="postnr",
        description="EAID_8F8BACBF_E985_4dc1_BCF4_27F5C3FD0BB1",
    )
    postal_code_division: Optional[str] = Field(
        None,
        alias="postnummerinddeling",
        description="EAID_E5F5DDF9_3CF4_4304_B02D_E67AB0CDD619",
    )
