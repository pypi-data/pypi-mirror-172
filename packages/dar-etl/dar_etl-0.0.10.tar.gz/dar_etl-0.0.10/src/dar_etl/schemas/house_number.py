from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class HouseNumber(DarBaseModel):
    access_addresses_designation: Optional[str] = Field(
        None,
        alias="adgangsadressebetegnelse",
        description="EAID_EDCC14FC_63ED_4ebe_8B52_3E406831A148",
    )
    access_point: Optional[str] = Field(
        None,
        alias="adgangspunkt",
        description="EAID_E3A37E0C_D0D8_4c30_BBD5_2F26F7A24591",
    )
    house_number_direction: Optional[str] = Field(
        None,
        alias="husnummerretning",
        description="EAID_1A906922_EFAC_4182_AA8C_08332D52C6EE",
    )
    house_number_text: Optional[str] = Field(
        None,
        alias="husnummertekst",
        description="EAID_83A4C230_5C5A_4ffb_B136_0315DD9F8DBE",
    )
    waypoint: Optional[str] = Field(
        None,
        alias="vejpunkt",
        description="EAID_F6BAEBD6_0306_4641_9DEA_C1441D986AFB",
    )
    piece_of_land: Optional[str] = Field(
        None,
        alias="jordstykke",
        description="EAID_dst052F4B_D60C_4ccd_BAE5_6BCED78FE40C",
    )
    placed_on_a_temporary_plot_of_land: Optional[str] = Field(
        None,
        alias="placeretPåForeløbigtJordstykke",
        description="EAID_dstC82C82_CC9D_4d7d_9B8A_8F4A1ADFB5AE",
    )
    geo_danmark_building: Optional[str] = Field(
        None,
        alias="geoDanmarkBygning",
        description="EAID_dst3C28C5_D640_4bc0_9014_FDC7CBF30581",
    )
    access_to_building: Optional[str] = Field(
        None,
        alias="adgangTilBygning",
        description="EAID_dst3E4349_6115_4191_AF4F_243CCE561C41",
    )
    access_to_technical_facilities: Optional[str] = Field(
        None,
        alias="adgangTilTekniskAnlæg",
        description="EAID_dst79A4C1_23B2_4c0c_85CC_60C6E2EA5AE0",
    )
    road_midpoint: Optional[str] = Field(
        None,
        alias="vejmidte",
        description="EAID_dstC9842D_CF82_4dc5_8114_3FF7AEF90C17",
    )
    voting_area: Optional[str] = Field(
        None,
        alias="afstemningsområde",
        description="EAID_dstB6088D_EE9E_451c_8070_088AA4520FA6",
    )
    municipal_division: Optional[str] = Field(
        None,
        alias="kommuneinddeling",
        description="EAID_dst714AB4_FE21_446f_BEE5_7AE65691A45B",
    )
    parish_council_voting_area: Optional[str] = Field(
        None,
        alias="menighedsrådsafstemningsområde",
        description="EAID_dst08DF20_7055_4542_8D3D_F8FCCD9A7125",
    )
    parish_division: Optional[str] = Field(
        None,
        alias="sogneinddeling",
        description="EAID_dst0864F0_E380_4aa6_A644_25974107FC47",
    )
    supplermentary_city_name: Optional[str] = Field(
        None,
        alias="supplerendeBynavn",
        description="EAID_dstF5C960_23DB_454c_A8A8_41B231DF61C7",
    )
    named_road: Optional[str] = Field(
        None,
        alias="navngivenVej",
        description="EAID_dst74C4B5_0F0F_4a51_B317_BA74938B605F",
    )
    postal_code: Optional[str] = Field(
        None,
        alias="postnummer",
        description="EAID_dst3F5BA7_EB6C_47a2_AC4B_90C72D4F3585",
    )
