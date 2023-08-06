from energium_protocol_sdk.fields.base import EnergiumField


class Id(EnergiumField, str):
    code = "PI"


class Name(EnergiumField, str):
    code = "PN"


class Sex(EnergiumField, str):
    code = "PS"


class Age(EnergiumField, str):
    code = "PA"


class Room(EnergiumField, str):
    code = "PR"


class OperationalOrKiosk(EnergiumField, str):
    """GNT-9 can give results on "operational side" or "kiosk" side*
    Possible values are Y and N
    Y - default and means "operational" side
    N - means "kiosk" side
    """
    code = "PC"
