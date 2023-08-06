from datetime import datetime
from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class NamedRoad(DarBaseModel):
    administreres_af_kommune: Optional[str] = Field(
        None,
        alias="administreresAfKommune",
        description="EAID_31D3BE04_2F70_4092_8381_5517A5543634",
    )
    description: Optional[str] = Field(None, description="EAID_C132D872_7F07_4ebf_BC6B_37049F2E5EB8")
    pronounced_street_name: Optional[str] = Field(
        None,
        alias="udtaltVejnavn",
        description="EAID_788F8478_A747_412d_9DE6_FEE0DB4C1BFA",
    )
    road_address_name: Optional[str] = Field(None, description="EAID_9621DD9D_50E3_4426_AB5A_A5E43DED4B05")
    street_name: Optional[str] = Field(None, description="EAID_CA00150C_5B5C_4c32_AE72_A7EE5AEDE015")
    road_name_location_origin_source: Optional[str] = Field(
        None,
        alias="vejnavnebeliggenhed_oprindelse_kilde",
        description="EAID_4C594A8E_797B_40bb_B60D_0E5C9159DCD3.EAID_7F8EB510_AD02_4fd5_844B_C9AB17FB1798.EAID_FD77FC95_714B_4779_B7FA_F9BBAB41758D",
    )
    road_name_location_origin_accuracy_class: Optional[str] = Field(
        None,
        alias="vejnavnebeliggenhed_oprindelse_nøjagtighedsklasse",
        description="EAID_4C594A8E_797B_40bb_B60D_0E5C9159DCD3.EAID_7F8EB510_AD02_4fd5_844B_C9AB17FB1798.EAID_B8A27494_DF27_4aa9_B1F4_EBD68D2479A5",
    )
    road_name_location_origin_registration: Optional[datetime] = Field(
        None,
        alias="vejnavnebeliggenhed_oprindelse_registrering",
        description="EAID_4C594A8E_797B_40bb_B60D_0E5C9159DCD3.EAID_7F8EB510_AD02_4fd5_844B_C9AB17FB1798.EAID_10DCC555_0BE9_4991_AD8C_DEA595CB08A0",
    )
    road_name_location_origin_technical_standard: Optional[str] = Field(
        None,
        alias="vejnavnebeliggenhed_oprindelse_tekniskStandard",
        description="EAID_4C594A8E_797B_40bb_B60D_0E5C9159DCD3.EAID_7F8EB510_AD02_4fd5_844B_C9AB17FB1798.EAID_181528AD_2DA3_4e9d_BF38_81916A924D2A",
    )
    road_name_location_road_name_line: Optional[str] = Field(
        None,
        alias="vejnavnebeliggenhed_vejnavnelinje",
        description="EAID_4C594A8E_797B_40bb_B60D_0E5C9159DCD3.EAID_93C24B4D_0641_4073_B260_1EC7F2024CF4",
    )
    road_name_location_road_name_area: Optional[str] = Field(
        None,
        alias="vejnavnebeliggenhed_vejnavneområde",
        description="EAID_4C594A8E_797B_40bb_B60D_0E5C9159DCD3.EAID_1C496CD9_4541_4574_974D_B641F186077F",
    )
    road_name_location_road_connection_points: Optional[str] = Field(
        None,
        alias="vejnavnebeliggenhed_vejtilslutningspunkter",
        description="EAID_4C594A8E_797B_40bb_B60D_0E5C9159DCD3.EAID_C3E042F2_A66E_40f4_92A1_7C7024A30D16",
    )
