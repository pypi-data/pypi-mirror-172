from datetime import datetime
from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class AddressPoint(DarBaseModel):
    origin_source: Optional[str] = Field(
        None,
        alias="oprindelse_kilde",
        description="EAID_B9AAE6C5_974D_4d20_BABA_C62874774F4B.EAID_FD77FC95_714B_4779_B7FA_F9BBAB41758D",
    )
    origin_accuracy_class: Optional[str] = Field(
        None,
        alias="oprindelse_nøjagtighedsklasse",
        description="EAID_B9AAE6C5_974D_4d20_BABA_C62874774F4B.EAID_B8A27494_DF27_4aa9_B1F4_EBD68D2479A5",
    )
    origin_registration: Optional[datetime] = Field(
        None,
        alias="oprindelse_registrering",
        description="EAID_B9AAE6C5_974D_4d20_BABA_C62874774F4B.EAID_10DCC555_0BE9_4991_AD8C_DEA595CB08A0",
    )
    origin_technical_standard: Optional[str] = Field(
        None,
        alias="oprindelse_tekniskStandard",
        description="EAID_B9AAE6C5_974D_4d20_BABA_C62874774F4B.EAID_181528AD_2DA3_4e9d_BF38_81916A924D2A",
    )
    position: Optional[str] = Field(
        None,
        alias="position",
        description="EAID_4B062EDE_CE8C_414b_AB85_B5A1FD72AA78",
    )
