EDIT_OPTIONS = [
    "start",
    "repeat",
    "single",
    "colors",
    "speed",
    "score",
    "destroyallDisabled",
    "showskull",
    "dieatend",
    "crashonload",
]

VERSIONS = {
    "deluxe": b'\x02',
    "revenge_beta01": b'\x0c',
    "revenge_beta02": b'\x0e',
    "revenge_final": b'\x0f'
}

_0E_0F_OFFSETS = {
    "start": 0x09,
    "repeat": 0x11,
    "single": 0x15,
    "colors": 0x19,
    "speed": 0x1D,
    "score": 0x2D,
    "destroyallDisabled": 0xB7,
    "showskull": 0xB8,
    "dieatend": 0xB9,
    "crashonload": 0xBA,
}

PROPERTY_TYPES = {
    "start": "int",
    "repeat": "int",
    "single": "int",
    "colors": "int",
    "speed": "float",
    "score": "int",
    "destroyallDisabled": "bool",
    "showskull": "bool",
    "dieatend": "bool",
    "crashonload": "bool",
}

OFFSETS = {
    b"\x0e": _0E_0F_OFFSETS,
    b"\x0f": _0E_0F_OFFSETS,
    b'\x0c': {
        # not yet researched
        "start": 0x00,
        "repeat": 0x00,
        "single": 0x00,
        "colors": 0x00,
        "speed": 0x00,
        "score": 0x00,
        "destroyallDisabled": 0x00,
        "showskull": 0x00,
        "dieatend": 0x00,
        "crashonload": 0x00,
    }
}