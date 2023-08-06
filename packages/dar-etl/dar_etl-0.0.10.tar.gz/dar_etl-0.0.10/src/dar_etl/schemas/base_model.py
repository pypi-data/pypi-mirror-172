from datetime import datetime
from enum import Enum
import logging
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Status(Enum):
    """https://danmarksadresser.dk/adressedata/kodelister/livscyklus/"""

    internal_preperation = "1"
    preliminary = "2"
    applicable = "3"
    discontinued = "4"
    archived = "5"
    deleted = "6"
    not_in_use = "7"
    in_use = "8"
    obsolete = "9"
    expired = "10"
    terminated = "11"


class BusinessProcess(Enum):
    """https://danmarksadresser.dk/adressedata/kodelister/forretningsproces"""

    master_data = "0"  # Stamdata
    address_assignment = "1"  # Adresseopgave
    dialog_client = "2"  # Dialogklient
    street_postcode = "3"  # Gadepostnummer
    supplementary_city_name = "4"  # Supplerendebynavn
    error_reporting_client = "5"  # Fejlmeldeklient
    undone_forward_dating = "6"  # Fortrudt fremdatering


class BusinessArea(Enum):
    dar = "54.15.10.25"  # Danmarks Adresse Register, DAR
    postal_codes = "54.15.10.15"  # Postnumre
    road_names_and_road_codes = "54.15.10.06"  # Vejnavne og vejkoder
    house_number = "54.15.10.07"  # Husnummer
    addresses = "54.15.10.08"  # Adresser
    unknown = "unknown"
    unknown1 = "10.00.00.00"
    unknown2 = "00.00.00.00"

    @classmethod
    def _missing_(cls, missing: object) -> Enum:  # noqa: WP526 WPS120
        logging.warning("%s does not have member '%s', assigning 'unknown'.", cls.__qualname__, str(missing))
        return cls(cls.unknown)


class BusinessEvent(Enum):
    named_road = "0"  # Navngivenvej
    named_road_municipal_district = "1"  # NavngivenvejKommunedel
    address = "2"  # Adresse
    house_number = "3"  # Husnummer
    postal_code = "4"  # Postnummer
    supplementary_city_name = "5"  # Supplerendebynavn
    house_number_reservation = "6"  # Husnummerreservation
    road_name_reservation = "7"  # VejnavnReservation
    address_assignment = "8"  # Adresseopgave
    address_assignment_item = "9"  # Adresseopgavegenstand
    dagi_municipality = "10"  # DAGIKommune
    dagi_parish_division = "11"  # DAGISogneinddeling
    dagi_postal_code = "12"  # DAGIPostnummer
    dagi_voting_area = "13"  # DAGIAfstemningsområde
    dagi_parish_council_voting_area = "14"  # DAGIMeninghedsrådsafstemningsområde
    dagi_supplementary_city_name = "15"  # DAGISupplerendeBynavn
    bbr_building = "16"  # BBRBygning
    bbr_technical_plant = "17"  # BBRTekniskanlæg
    mu_piece_of_land = "18"  # MUJordstykke (matriklens udvidelse)
    geo_danmark_building = "19"  # GeoDanmarkBygning
    geo_danmark_waypoint = "20"  # GeoDanmarkVejmidte
    unknown = "unknown"

    @classmethod
    def _missing_(cls, missing: object) -> Enum:  # noqa: WP526 WPS120
        if str(missing) == "NavngivenVej":
            return cls.named_road
        logging.warning("%s does not have member '%s', assigning 'unknown'.", cls.__qualname__, str(missing))
        return cls(cls.unknown)


class DarBaseModel(BaseModel):
    business_event: Optional[BusinessEvent] = Field(
        None,
        alias="forretningshændelse",
        description="Den forretningshændelse, som afstedkom opdateringen af adresseelementet til den pågældende version",
    )
    business_area: Optional[BusinessArea] = Field(
        None,
        alias="forretningsområde",
        description="Det forretningsområde som har opdateret adresseelementet til den pågældende version",
    )
    business_process: Optional[BusinessProcess] = Field(
        None,
        alias="forretningsproces",
        description="Den forretningsproces, som afstedkom opdateringen af adresseelementet til den pågældende version",
    )
    id_namespace: Optional[str] = Field(
        None,
        alias="id_namespace",
        description="EAID_D273E3D8_A3F4_41bc_AF9C_E67B4A29C008.EAID_6CEB0356_5CBF_4159_B96B_A2489DD2DAC8",
    )
    id_local: Optional[str] = Field(
        None,
        alias="id_lokalId",
        description="Identifikation af adresseelementet igennem hele dets livscyklus.",
    )
    registration_from: Optional[datetime] = Field(
        None,
        alias="registreringFra",
        description="Tidspunktet hvor registreringen af den pågældende version af adresseelementet er foretaget",
    )
    registration_operator: Optional[str] = Field(
        None,
        description="Den aktør der har foretaget registreringen af den pågældende version af adresseelementet",
        alias="registreringsaktør",
    )
    registration_to: Optional[datetime] = Field(
        None,
        alias="registreringTil",
        description="Tidspunktet hvor en ny registrering på adresseelementet er foretaget, og hvor denne version således ikke længere er den seneste.",
    )
    status: Optional[Status] = Field(
        None,
        alias="status",
        description="Adresseelementets status i den pågældende version, dvs. elementets tilstand i den samlede livscyklus",
    )
    effect_from: Optional[datetime] = Field(
        None,
        alias="virkningFra",
        description="Tidspunktet hvorfra den pågældende version af adresseelementet har virkning",
    )
    effect_to: Optional[datetime] = Field(
        None,
        alias="virkningTil",
        description="Tidspunktet hvor virkningen af den pågældende version af adresseelementet ophører",
    )
    effector: Optional[str] = Field(
        None,
        alias="virkningsaktør",
        description="Den aktør der har afstedkommet virkningsegenskaberne for den pågældende version af adresseelementet",
    )
