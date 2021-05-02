"""add user bitschema attribute

Revision ID: 1272e4b54a32
Revises: 
Create Date: 2021-04-18 12:49:18.152022

"""
from alembic import op
from app.database.db_types.JsonCustomType import JsonCustomType
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1272e4b54a32"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(sa.Column("additional_info", JsonCustomType, nullable=True))
        batch_op.add_column(
            sa.Column("is_organization_rep", sa.Boolean(), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "timezone",
                sa.Enum(
                    "AFRICA_ABIDJAN",
                    "AFRICA_ACCRA",
                    "AFRICA_ADDIS_ABABA",
                    "AFRICA_ALGIERS",
                    "AFRICA_ASMARA",
                    "AFRICA_ASMERA",
                    "AFRICA_BAMAKO",
                    "AFRICA_BANGUI",
                    "AFRICA_BANJUL",
                    "AFRICA_BISSAU",
                    "AFRICA_BLANTYRE",
                    "AFRICA_BRAZZAVILLE",
                    "AFRICA_BUJUMBURA",
                    "AFRICA_CAIRO",
                    "AFRICA_CASABLANCA",
                    "AFRICA_CEUTA",
                    "AFRICA_CONAKRY",
                    "AFRICA_DAKAR",
                    "AFRICA_DAR_ES_SALAAM",
                    "AFRICA_DJIBOUTI",
                    "AFRICA_DOUALA",
                    "AFRIKA_EL_AAIUN",
                    "AFRICA_FREETOWN",
                    "AFRICA_GABORONE",
                    "AFRICA_HARARE",
                    "AFRICA_JOHANNESBURG",
                    "AFRICA_JUBA",
                    "AFRICA_KAMPALA",
                    "AFRICA_KHARTOUM",
                    "AFRICA_KIGALI",
                    "AFRICA_KINSHASA",
                    "AFRICA_LAGOS",
                    "AFRICA_LIBREVILLE",
                    "AFRICA_LOME",
                    "AFRICA_LUANDA",
                    "AFRICA_LUBUMBASHI",
                    "AFRICA_LUSAKA",
                    "AFRICA_MALABO",
                    "AFRICA_MAPUTO",
                    "AFRIKA_MASERU",
                    "AFRICA_MBABANE",
                    "AFRICA_MOGADISHU",
                    "AFRICA_MONROVIA",
                    "AFRICA_NAIROBI",
                    "AFRICA_NDJAMENA",
                    "AFRICA_NIAMEY",
                    "AFRICA_NOUAKCHOTT",
                    "AFRICA_OUAGADOUGOU",
                    "AFRICA_PORTO_NOVO",
                    "AFRICA_SAO_TOME",
                    "AFRICA_TIMBUKTU",
                    "AFRICA_TRIPOLI",
                    "AFRICA_TUNIS",
                    "AFRICA_WINDHOEK",
                    "AMERICA_ADAK",
                    "AMERICA_ANCHORAGE",
                    "AMERICA_ANGUILLA",
                    "AMERICA_ANTIGUA",
                    "AMERICA_ARAGUAINA",
                    "AMERICA_ARGENTINA_BUENOS_AIRES",
                    "AMERICA_AGRGENTINA_CATAMARCA",
                    "AMERICA_ARGENTINA_COMODRIVADAVIA",
                    "AMERICA_ARGENTINA_CORDOBA",
                    "AMERICA_ARGENTINA_JUJUY",
                    "AMERICA_ARGENTINA_LA_RIOJA",
                    "AMERICA_ARGENTINA_MENDOZA",
                    "AMERICA_ARGENTINA_RIO_GALLEGOS",
                    "AMERICA_ARGENTINA_SALTA",
                    "AMERICA_ARGENTINA_SAN_JUAN",
                    "AMERICA_ARGENTINA_SAN_LUIS",
                    "AMERICA_ARGENTINA_TUCUMAN",
                    "AMERICA_ARGENTINA_USHUAIA",
                    "AMERICA_ARUBA",
                    "AMERICA_ASUNCION",
                    "AMERICA_ATIKOKAN",
                    "AMERICA_ATKA",
                    "AMERICA_BAHIA",
                    "AMERICA_BAHIA_BANDERAS",
                    "AMERICA_BARBADOS",
                    "AMERICA_BELEM",
                    "AMERICA_BELIZE",
                    "AMERICA_BLANC_SABLON",
                    "AMERICA_BOA_VISTA",
                    "AMERICA_BOGOTA",
                    "AMERICA_BOISE",
                    "AMERICA_BUENOS_AIRES",
                    "AMERICA_CAMBRIDGE_BAY",
                    "AMERICA_CAMPO_GRANDE",
                    "AMERICA_CANCUN",
                    "AMERICA_CARACAS",
                    "AMERICA_CATAMARCA",
                    "AMERICA_CAYENNE",
                    "AMERICA_CAYMAN",
                    "AMERICA_CHICAGO",
                    "AMERICA_CHIHUAHUA",
                    "AMERICA_CORAL_HARBOUR",
                    "AMERICA_CORDOBA",
                    "AMERICA_COSTA_RICA",
                    "AMERICA_CRESTON",
                    "AMERICA_CUIABA",
                    "AMERICA_CURACAO",
                    "AMERICA_DANMARKSHAVN",
                    "AMERICA_DAWSON",
                    "AMERICA_DAWSON_CREEK",
                    "AMERICA_DENVER",
                    "AMERICA_DETROIT",
                    "AMERICA_DOMINICA",
                    "AMERICA_EDMONTON",
                    "AMERICA_EIRUNEPE",
                    "AMERICA_EL_SALVADOR",
                    "AMERICA_ENSENADA",
                    "AMERICA_FORT_NELSON",
                    "AMERICA_FORT_WAYNE",
                    "AMERICA_FORTALEZA",
                    "AMERICA_GLACE_BAY",
                    "AMERICA_GODTHAB",
                    "AMERICA_GOOSE_BAY",
                    "AMERICA_GRAND_TURK",
                    "AMERICA_GRENADA",
                    "AMERICA_GUADELOUPE",
                    "AMERICA_GUATEMALA",
                    "AMERICA_GUAYAQUIL",
                    "AMERICA_GUYANA",
                    "AMERICA_HALIFAX",
                    "AMERICA_HAVANA",
                    "AMERICA_HERMOSILLO",
                    "AMERICA_INDIANA_INDIANAPOLIS",
                    "AMERICA_INDIANA_KNOX",
                    "AMERICA_INDIANA_MARENGO",
                    "AMERICA_INDIANA_PETERSBURG",
                    "AMERICA_INDIANA_TELL_CITY",
                    "AMERICA_INDIANA_VEVAY",
                    "AMERICA_INDIANA_VINCENNES",
                    "AMERICA_INDIANA_WINAMAC",
                    "AMERICA_INDIANAPOLIS",
                    "AMERICA_INUVIK",
                    "AMERICA_IQALUIT",
                    "AMERICA_JAMAICA",
                    "AMERICA_JUJUY",
                    "AMERICA_JUNEAU",
                    "AMERICA_KENTUCKY_LOUISVILLE",
                    "AMERICA_KENTUCKY_MONTICELLO",
                    "AMERICA_KNOX_IN",
                    "AMERICA_KRALENDIJK",
                    "AMERICA_LA_PAZ",
                    "AMERICA_LIMA",
                    "AMERICA_LOS_ANGELES",
                    "AMERICA_LOUISVILLE",
                    "AMERICA_LOWER_PRINCES",
                    "AMERICA_MACEIO",
                    "AMERICA_MANAGUA",
                    "AMERICA_MANAUS",
                    "AMERICA_MARIGOT",
                    "AMERICA_MARTINIQUE",
                    "AMERICA_MATAMOROS",
                    "AMERICA_MAZATLAN",
                    "AMERICA_MENDOZA",
                    "AMERICA_MENOMINEE",
                    "AMERICA_MERIDA",
                    "AMERICA_METLAKATLA",
                    "AMERICA_MEXICO_CITY",
                    "AMERICA_MIQUELON",
                    "AMERICA_MONCTON",
                    "AMERICA_MONTERREY",
                    "AMERICA_MONTEVIDEO",
                    "AMERICA_MONTREAL",
                    "AMERICA_MONTSERRAT",
                    "AMERICA_NASSAU",
                    "AMERICA_NEW_YORK",
                    "AMERICA_NIPIGON",
                    "AMERICA_NOME",
                    "AMERICA_NORONHA",
                    "AMERICA_NORTH_DAKOTA_BEULAH",
                    "AMERICA_NORTH_DAKOTA_CENTER",
                    "AMERICA_NORTH_DAKOTA_NEW_SALEM",
                    "AMERICA_DJINAGA",
                    "AMERICA_PANAMA",
                    "AMERICA_PANGNIRTUNG",
                    "AMERICA_PARAMARIBO",
                    "AMERICA_PHOENIX",
                    "AMERICA_PORT_AU_PRINCE",
                    "AMERICA_PORT_OF_SPAIN",
                    "AMERICA_PORTO_ACRE",
                    "AMERICA_PORTO_VELHO",
                    "AMERICA_PUERTO_RICO",
                    "AMERICA_PUNTA_ARENAS",
                    "AMERICA_RAINY_RIVER",
                    "AMERICA_RANKIN_INLET",
                    "AMERICA_RECIFE",
                    "AMERICA_REGINA",
                    "AMERICA_RESOLUTE",
                    "AMERICA_RIO_BRANCO",
                    "AMERICA_ROSARIO",
                    "AMERICA_SANTA_ISABEL",
                    "AMERICA_SANTAREM",
                    "AMERICA_SANTIAGO",
                    "AMERICA_SANTO_DOMINGO",
                    "AMERICA_SAO_PAULO",
                    "AMERICA_SCORESBYSUND",
                    "AMERICA_SHIPROCK",
                    "AMERICA_SITKA",
                    "AMERICA_ST_BARTHELEMY",
                    "AMERICA_ST_JOHNS",
                    "AMERICA_ST_KITTS",
                    "AMERICA_ST_LUCIA",
                    "AMERICA_ST_THOMAS",
                    "AMERICA_ST_VINCENT",
                    "AMERICA_SWIFT_CURRENT",
                    "AMERICA_TEGUCIGALPA",
                    "AMERICA_THULE",
                    "AMERICA_THUNDER_BAY",
                    "AMERICA_TIJUANA",
                    "AMERICA_TORONTO",
                    "AMERICA_TORTOLA",
                    "AMERICA_VANCOUVER",
                    "AMERICA_VIRGIN",
                    "AMERICA_WHITEHORSE",
                    "AMERICA_WINNIPEG",
                    "AMERICA_YAKUTAT",
                    "AMERICA_YELLOWKNIFE",
                    "ANTARCTICA_CASEY",
                    "ANTARCTICA_DAVIS",
                    "ANTARCTICA_DUMONTDURVILLE",
                    "ANTARCTICA_MACQUARIE",
                    "ANTARCTICA_MAWSON",
                    "ANTARCTICA_MCMURDO",
                    "ANTARCTICA_PALMER",
                    "ANTARCTICA_ROTHERA",
                    "ANTARCTICA_SOUTH_POLE",
                    "ANTARCTICA_SYOWA",
                    "ANTARCTICA_TROLL",
                    "ANTARCTICA_VOSTOK",
                    "ARCTIC_LONGYEARBYEN",
                    "ASIA_ADEN",
                    "ASIA_ALMATY",
                    "ASIA_AMMAN",
                    "ASIA_ANADYR",
                    "ASIA_AQTAU",
                    "ASIA_AQTOBE",
                    "ASIA_ASHGABAT",
                    "ASIA_ASHKHABAD",
                    "ASIA_ATYRAU",
                    "ASIA_BAGHDAD",
                    "ASIA_BAHRAIN",
                    "ASIA_BAKU",
                    "ASIA_BANGKOK",
                    "ASIA_BARNAUL",
                    "ASIA_BEIRUT",
                    "ASIA_BISHKEK",
                    "ASIA_BRUNEI",
                    "ASIA_CALCUTTA",
                    "ASIA_CHITA",
                    "ASIA_CHOIBALSAN",
                    "ASIA_CHONGQING",
                    "ASIA_CHUNGKING",
                    "ASIA_COLOMBO",
                    "ASIA_DACCA",
                    "ASIA_DAMASCUS",
                    "ASIA_DHAKA",
                    "ASIA_DILI",
                    "ASIA_DUBAI",
                    "ASIA_DUSHANBE",
                    "ASIA_FAMAGUSTA",
                    "ASIA_GAZA",
                    "ASIA_HARBIN",
                    "ASIA_HEBRON",
                    "ASIA_HO_CHI_MIN",
                    "ASIA_HONGKONG",
                    "ASIA_HOVD",
                    "ASIA_IRKUTSK",
                    "ASIA_ISTANBUL",
                    "ASIA_JAKARTA",
                    "ASIA_JAYAPURA",
                    "ASIA_JERUSSALEM",
                    "ASIA_KABUL",
                    "ASIA_KAMCHATKA",
                    "ASIA_KARACHI",
                    "ASIA_KASHGAR",
                    "ASIA_KATHMANDU",
                    "ASIA_KATMANDU",
                    "ASIA_KHANDYGA",
                    "ASIA_KOLKATA",
                    "ASIA_KRASNOYARSK",
                    "ASIA_KUALA_LUMPUR",
                    "ASIA_KUCHING",
                    "ASIA_KUWAIT",
                    "ASIA_MACAO",
                    "ASIA_MACAU",
                    "ASIA_MAGADAN",
                    "ASIA_MAKASSAR",
                    "ASIA_MANILA",
                    "ASIA_MUSCAT",
                    "ASIA_NICOSIA",
                    "ASIA_NOVOKUZNEETSK",
                    "ASIA_NOVOSIBIRSK",
                    "ASIA_OMSK",
                    "ASIA_ORAL",
                    "ASIA_PHNOM_PENH",
                    "ASIA_PONTIANAK",
                    "ASIA_PYONGYANG",
                    "ASIA_QATAR",
                    "ASIA_QYZYLORDA",
                    "ASIA_RANGOON",
                    "ASIA_RIYADH",
                    "ASIA_SAIGON",
                    "ASIA_SAKHALIN",
                    "ASIA_SAMARKAND",
                    "ASIA_SEOUL",
                    "ASIA_SHANGHAI",
                    "ASIA_SINGAPORE",
                    "ASIA_SREDNEKOLYMSK",
                    "ASIA_TAIPEI",
                    "ASIA_TASHKENT",
                    "ASIA_TBILISI",
                    "ASIA_TEHRAN",
                    "ASIA_TEL_AVIV",
                    "ASIA_THIMBU",
                    "ASIA_THIMPHU",
                    "ASIA_TOKYO",
                    "ASIA_TOMSK",
                    "ASIA_UJUNG_PANDANG",
                    "ASIA_ULAANBAATAR",
                    "ASIA_ULAN_BATOR",
                    "ASIA_URUMQI",
                    "ASIA_UST_NERA",
                    "ASIA_VIENTIANE",
                    "ASIA_VLADIVOSTOK",
                    "ASIA_YAKUTSK",
                    "ASIA_YANGON",
                    "ASIA_YEKATERINBURG",
                    "ASIA_YEREVAN",
                    "ATLANTIC_AZORES",
                    "ATLANTIC_BERMUDA",
                    "ATLANTIC_CANARY",
                    "ATLANTIC_CAPE_VERDE",
                    "ATLANTIC_FAEROE",
                    "ATLANTIC_FAROE",
                    "ATLANTIC_JAN_MAYEN",
                    "ATLANTIC_MADEIRA",
                    "ATLANTIC_REYKJAVIK",
                    "ATLANTIC_SOUTH_GEORGIA",
                    "ATLANTIC_ST_HELENA",
                    "ATLANTIC_STANLEY",
                    "AUSTRALIA_ACT",
                    "AUSTRALIA_ADELAIDE",
                    "AUSTRALIA_BRISBANE",
                    "AUSTRALIA_BROKEN_HILL",
                    "AUSTRALIA_CANBERRA",
                    "AUSTRALIA_CURRIE",
                    "AUSTRALIA_DARWIN",
                    "AUSTRALIA_EUCLA",
                    "AUSTRALIA_HOBART",
                    "AUSTRALIA_LHI",
                    "AUSTRALIA_LINDEMAN",
                    "AUSTRALIA_LORD_HOWE",
                    "AUSTRALIA_MELBOURNE",
                    "AUSTRALIA_NSW",
                    "AUSTRALIA_NORTH",
                    "AUSTRALIA_PERTH",
                    "AUSTRALIA_QUEENSLAND",
                    "AUSTRALIA_SOUTH",
                    "AUSTRALIA_SYDNEY",
                    "AUSTRALIA_TASMANIA",
                    "AUSTRALIA_VICTORIA",
                    "AUSTRALIA_WEST",
                    "AUSTRALIA_YANCOWINNA",
                    "BRAZIL_ACREE",
                    "BRAZIL_DENORONHA",
                    "BRAZIL_EAST",
                    "BRAZIL_WEST",
                    "CET",
                    "CST6CDT",
                    "CANADA_ATLANTIC",
                    "CANADA_CENTRAL",
                    "CANADA_EASTERN",
                    "CANADA_MOUNTAIN",
                    "CANADA_NEWFOUNDLAND",
                    "CANADA_PACIFIC",
                    "CANADA_SASKATCHEWAN",
                    "CANADA_YUKON",
                    "CHILE_CONTINEENTAL",
                    "CHILE_EASTERISLAND",
                    "CUBA",
                    "EET",
                    "EST",
                    "EST5EDT",
                    "EGYPT",
                    "EIRE",
                    "ETC_GMT",
                    "ETC_GMT_PLUS_0",
                    "ETC_GMT_PLUS_1",
                    "ETC_GMT_PLUS_10",
                    "ETC_GMT_PLUS_11",
                    "ETC_GMT_PLUS_12",
                    "ETC_GMT_PLUS_2",
                    "ETC_GMT_PLUS_3",
                    "ETC_GMT_PLUS_4",
                    "ETC_GMT_PLUS_5",
                    "ETC_GMT_PLUS_6",
                    "ETC_GMT_PLUS_7",
                    "ETC_GMT_PLUS_8",
                    "ETC_GMT_PLUS_9",
                    "ETC_GMT_MINUS_0",
                    "ETC_GMT_MINUS_1",
                    "ETC_GMT_MINUS_10",
                    "ETC_GMT_MINUS_11",
                    "ETC_GMT_MINUS_12",
                    "ETC_GMT_MINUS_13",
                    "ETC_GMT_MINUS_14",
                    "ETC_GMT_MINUS_2",
                    "ETC_GMT_MINUS_3",
                    "ETC_GMT_MINUS_4",
                    "ETC_GMT_MINUS_5",
                    "ETC_GMT_MINUS_6",
                    "ETC_GMT_MINUS_7",
                    "ETC_GMT_MINUS_8",
                    "ETC_GMT_MINUS_9",
                    "ETC_GMT_0",
                    "ETC_GREEENWICH",
                    "ETC_UCT",
                    "ETC_UTC",
                    "ETC_UNIVERSAL",
                    "ETC_ZULU",
                    "EUROPE_AMSTERDAM",
                    "EUROPE_ANDORRA",
                    "EUROPE_ASTRAKHAN",
                    "EUROPE_ATHENS",
                    "EUROPE_BELFAST",
                    "EUROPE_BELGRADE",
                    "EUROPE_BERLIN",
                    "EUROPE_BRATISLAVA",
                    "EUROPE_BRUSSELS",
                    "EUROPE_BUCHAREST",
                    "EUROPE_BUDAPEST",
                    "EUROPE_BUSINGEN",
                    "EUROPE_CHISINAU",
                    "EUROPE_COPENHAGEN",
                    "EUROPE_DUBLIN",
                    "EUROPE_GIBRALTAR",
                    "EUROPE_GUERNSEY",
                    "EUROPE_HELSINKI",
                    "EUROPE_ISLE_OF_MAN",
                    "EUROPE_ISTANBUL",
                    "EUROPE_JERSEY",
                    "EUROPE_KALININGRAD",
                    "EUROPE_KIEV",
                    "EUROPE_KIROV",
                    "EUROPE_LISBON",
                    "EUROPE_LJUBLJANA",
                    "EUROPE_LONDON",
                    "EUROPE_LUXEMBORG",
                    "EUROPE_MADRID",
                    "EUROPE_MALTA",
                    "EUROPE_MARIEHAMN",
                    "EUROPE_MINSK",
                    "EUROPE_MONACO",
                    "EUROPE_MOSCOW",
                    "EUROPE_NICOSSIA",
                    "EUROPE_OSLO",
                    "EUROPE_PARIS",
                    "EUROPE_PODGORICA",
                    "EUROPE_PRAGUE",
                    "EUROPE_RIGA",
                    "EUROPE_ROME",
                    "EUROPE_SAMARA",
                    "EUROPE_SAN_MARINO",
                    "EUROPE_SARAJEVO",
                    "EUROPE_SARATOV",
                    "EUROPE_SIMFEROPOL",
                    "EUROPE_SKOPJE",
                    "EUROPE_SOFIA",
                    "EUROPE_STOCKHOLM",
                    "EUROPE_TALLINN",
                    "EUROPE_TIRANE",
                    "EUROPE_TIRASPOL",
                    "EUROPE_ULYANOVSK",
                    "EUROPE_UZHGROD",
                    "EUROPE_VADUZ",
                    "EUROPE_VATICAN",
                    "EUROPE_VIENNA",
                    "EUROPE_VILNIUS",
                    "EUROPE_VOLGOGRAD",
                    "EUROPE_WARSAW",
                    "EUROPE_ZAGREB",
                    "EUROPE_ZAPOROZHYE",
                    "EUROPE_ZURICH",
                    "GB",
                    "GB_EIRE",
                    "GMT",
                    "GMT_PLUS_0",
                    "GMT_MINUS_0",
                    "GMT0",
                    "GREEENWICH",
                    "HST",
                    "HONGKONG",
                    "ICELAND",
                    "INDIAN_ANTANANARIVO",
                    "INDIAN_CHAGOS",
                    "INDIAN_CHRISTMAS",
                    "INDIAN_COCOS",
                    "INDIAN_COMORO",
                    "INDIAN_KARGUELEN",
                    "INDIAN_MAHE",
                    "INDIAN_MALDIVES",
                    "INDIAN_MAURITIUS",
                    "INDIAN_MAYOTTE",
                    "INDIAN_REUNION",
                    "IRAN",
                    "ISRAEL",
                    "JAMAICA",
                    "JAPAN",
                    "KWAJALEIN",
                    "LIBYA",
                    "MET",
                    "MST",
                    "MST7MDT",
                    "MEXICO_BAJANORTE",
                    "MEXICO_BAJASUR",
                    "MEXICO_GENERAL",
                    "NZ",
                    "NZ_CHAT",
                    "NAVAJO",
                    "PRC",
                    "PST8PDT",
                    "PACIFIC_APIA",
                    "PACIFIC_AUCKLAND",
                    "PACIFIC_BOUGAINVILLE",
                    "PACIFIC_CHATHAM",
                    "PACIFIC_CHUUK",
                    "PACIFIC_EASTER",
                    "PACIFIC_EFATE",
                    "PACIFIC_ENDERBURY",
                    "PACIFIC_FAKAOFO",
                    "PACIFIC__FIJI",
                    "PACIFIC_FUNAFUTI",
                    "PACIFIC_GALAPAGOS",
                    "PACIFIC_GAMBIER",
                    "PACIFIC_GUADALCANAL",
                    "PACIFIC_GUAM",
                    "PACIFIC_HONOLULU",
                    "PACIFIC_JOHNSTON",
                    "PACIFIC_KIRITIMATI",
                    "PACIFIC_KOSRAE",
                    "PACIFIC_KWAJALEIN",
                    "PACIFIC_MAJURO",
                    "PACIFIC_MARQUESAS",
                    "PACIFIC_MIDWAY",
                    "PACIFIC_NAURU",
                    "PACIFIC_NIUE",
                    "PACIFIC_NORFOLK",
                    "PACIFIC_NOUMEA",
                    "PACIFIC_PAGO_PAGO",
                    "PACIFIC_PALAU",
                    "PACIFIC_PITCAIRN",
                    "PACIFIC_POHNPEI",
                    "PACIFIC_PONAPE",
                    "PACIFIC_PORT_MORESBY",
                    "PACIFIC_RAROTONGA",
                    "PACIFIC_SAIPAN",
                    "PACIFIC_SAMOA",
                    "PACIFIC_TAHITI",
                    "PACIFIC_TARAWA",
                    "PACIFIC_TONGATAPU",
                    "PACIFIC_TRUK",
                    "PACIFIC_WAKE",
                    "PACIFIC_WALLIS",
                    "PACIFIC_YAP",
                    "POLAND",
                    "PORTUGAL",
                    "ROC",
                    "ROK",
                    "SINGAPORE",
                    "TURKEY",
                    "UCT",
                    "US_ALASKA",
                    "US_ALEUTIAN",
                    "US_ARIZONA",
                    "US_CENTRAL",
                    "US_EAST_INDIANA",
                    "US_EASTERN",
                    "US_HAWAII",
                    "US_INDIANA_STARKE",
                    "US_MICHIGAN",
                    "US_MOUNTAIN",
                    "US_PACIFIC",
                    "US_SAMOA",
                    "UTC",
                    "UNIVERSAL",
                    "W_SU",
                    "WET",
                    "ZULU",
                    name="timezone",
                ),
                nullable=True,
            )
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("timezone")
        batch_op.drop_column("is_organization_rep")
        batch_op.drop_column("additional_info")
