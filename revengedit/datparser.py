from struct import unpack
from revengedit.consts import OFFSETS, VERSIONS

class ParsingError(Exception): pass

def get_dat_version(filePath=str):
    file = open(filePath, 'rb+')
    file.seek(4)
    version = file.read(1)
    return version

def parse_file(filePath=str):
    """
    Parse a *.dat file and return a dict containing known level difficulty
    properties for the Zuma's Revenge! *.dat file format.
    """

    magic = b''
    
    start = int()
    repeat = int()
    single = int()
    colors = int()
    speed = float()
    score = int()

    destroyallDisabled = bool()
    showskull = bool()
    dieatend = bool()
    crashonload = bool()

    file = open(filePath, 'rb+')
    magic = file.read(4)
    if magic != b'CURV':
        raise ParsingError("magic is not CURV")
    version = get_dat_version(filePath)
    if version == VERSIONS["deluxe"]:
        raise ParsingError("file is for Zuma Deluxe")
    elif version == VERSIONS["revenge_beta02"] or version == VERSIONS["revenge_final"]:
        # file is for Zuma's Revenge, go on
        pass
    elif version == VERSIONS["revenge_beta01"]:
        # 0x0C is used in earlier builds of ZR; it has slightly different offsets
        raise ParsingError("version 0x0C not supported yet")
    else:
        raise ParsingError("invalid curv file")

    ### GENERAL PROPERTIES ###
    # start, repeat, single, colors, speed
    # offset comments will assume version 0x0E/0F
    
    file.seek(OFFSETS[version]["start"]) # start
    start = int.from_bytes(file.read(4), "little")

    # OFFSETS 0x11 - 0x1D
    file.seek(OFFSETS[version]["repeat"])
    repeat = int.from_bytes(file.read(4), "little")
    single = int.from_bytes(file.read(4), "little")
    colors = int.from_bytes(file.read(4), "little")
    speed = unpack('<f', file.read(4))[0]
    
    # score is at offset 0x2D
    # properties that precede it (offsets 0x21, 0x25 and 0x29)
    # are unknown
    file.seek(OFFSETS[version]["score"])
    score = int.from_bytes(file.read(4), "little")

    ### MISCELLANEOUS PROPERTIES ###
    # destroyall, showskull, dieatend, crashonload
    # note: everything but destroyall and dieatend has an "unofficial" name
    # since Deluxe uses xml, Revenge uses this awful binary format
    # that is integrated with the path itself. these property names
    # are for code / clarity reasons.
    
    # "dieatend" is taken from the decompiled source of Zuma's Revenge!
    # Flash version:
    #
    # Script: Zuma2App
    #  75  public var mAdAPI:MSNAdAPI;
    #  76
    # -77- public var gDieAtEnd:Boolean;
    #  78 
    #  79  public var mSharedObject:SharedObject;

    # Offsets 0xB7 - 0xBA
    file.seek(OFFSETS[version]["destroyallDisabled"])
    # destroyall is an inverted boolean (0 = true, 1 = false)
    destroyallDisabled = bool(int.from_bytes(file.read(1), "little"))
    showskull = bool(int.from_bytes(file.read(1), "little"))
    dieatend = bool(int.from_bytes(file.read(1), "little"))
    crashonload = bool(int.from_bytes(file.read(1), "little"))

    return {
        'file': filePath,
        'version': version,
        'start': start,
        'repeat': repeat,
        'single': single,
        'colors': colors,
        'speed': speed,
        'score': score,
        'destroyallDisabled': destroyallDisabled,
        'showskull': showskull,
        'dieatend': dieatend,
        'crashonload': crashonload,
    }