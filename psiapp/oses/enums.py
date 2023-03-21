from enum import Enum


class SelectOptions(Enum):
    DEFAULT = "", "Select an OS type"
    IOS = "ios", "IOS"
    IOSXE = "iosxe", "IOS-XE"
    NXOS = "nxos", "NXOS"
    ACI = "aci", "NXOS in ACI mode"
    ASA = "asa", "ASA"
    FTD = "ftd", "FTD"
    FMC = "fmc", "FMC"
    FXOS = "fxos", "FXOS"
