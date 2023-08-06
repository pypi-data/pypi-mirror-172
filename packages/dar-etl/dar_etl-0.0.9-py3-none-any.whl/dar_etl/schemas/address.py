from typing import Optional

from pydantic import Field

from dar_etl.schemas.base_model import DarBaseModel


class Adresse(DarBaseModel):
    door_designation: Optional[str] = Field(
        None,
        alias="dørbetegnelse",
        description="EAID_16B39B2F_0D4D_45ca_8164_8E1D78D202FC",
    )
    door_point: Optional[str] = Field(
        None,
        alias="dørpunkt",
        description="EAID_2E77B0C3_49AF_47b0_AD4E_DD653B99FD0B",
    )
    floor_designation: Optional[str] = Field(
        None,
        alias="etagebetegnelse",
        description="EAID_805BB835_641D_49d5_93E6_80C8E3FFD91C",
    )

    address_designation: Optional[str] = Field(
        None,
        alias="adressebetegnelse",
        description="EAID_BB398854_F92E_4372_A20A_D7136BB5CD9C",
    )
    building: Optional[str] = Field(
        None,
        alias="bygning",
        description="BBR bygning er relateret til husnummer og ikke til adressen, der er derfor ikke bagvedliggende data for denne parameter, og anvendelsen af parameteren vil ikke give noget resultat.",
    )
    house_number: Optional[str] = Field(
        None,
        alias="husnummer",
        description="Angiver det DAR husnummer (adgangsadresse), som adressen er tilknyttet. Bruger du dette inputparameteren finder du alle adresser for det pågældende husnummer",
    )
