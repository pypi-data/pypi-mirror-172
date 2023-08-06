from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class NamedRoadMunicipalDistrict(DarBaseModel):
    municipality: Optional[str] = Field(
        None,
        alias="kommune",
        description="EAID_0A04B5E9_9F12_49cb_B2AF_AFEE0315AE2B",
    )
    waycode: Optional[str] = Field(
        None,
        alias="vejkode",
        description="EAID_852A683F_3E30_4009_A003_B3C8F6F76930",
    )
    named_road: Optional[str] = Field(
        None,
        alias="navngivenVej",
        description="EAID_dstE87A3E_ECA3_4f38_A586_117287E4754A",
    )
