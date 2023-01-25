from enum import Enum


class PlaneEnum(str, Enum):
    """From https://www.airlines-inform.ru/commercial-aircraft/"""

    Airbus_A220 = "Airbus A220"
    Airbus_A310 = "Airbus A310"
    Airbus_A320 = "Airbus A320"
    Airbus_A330 = "Airbus A330"
    Airbus_A340 = "Airbus A340"
    Airbus_A350 = "Airbus A350"
    Airbus_A380 = "Airbus A380"

    Boeing_717 = "Boeing-717"
    Boeing_737 = "Boeing-737"
    Boeing_747 = "Boeing-747"
    Boeing_757 = "Boeing-757"
    Boeing_767 = "Boeing-767"
    Boeing_777 = "Boeing-777"
    Boeing_787 = "Boeing-787"

    ATR_42_72 = "ATR 42/72"
    Bae_Avro_RJ = "Bae Avro RJ"
    Bombardier_Dash_8 = "Bombardier Dash 8"
    Bombardier_CRJ = "Bombardier CRJ"
    Embraer_ERJ = "Embraer ERJ"
    Embraer_170_190 = "Embraer 170/190"
    Saab = "Saab"

    Superjet_100 = "Superjet-100"
    Topolev_Tu_204 = "Туполев Ту-204"
    Ilushin_Il_96 = "Ильюшин Ил-96"
    Ilushin_Il_114 = "Ильюшин Ил-114"
    Antonov_An_38 = "Антонов Ан-38"
    Antonov_An_140 = "Антонов Ан-140"
    Antonov_An_148 = "Антонов Ан-148"


class UserRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    PASSENGER = "PASSENGER"
