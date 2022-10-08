import re
from struct import pack
from argparse import ArgumentTypeError
from revengedit import consts
from revengedit.datparser import parse_file

def arg_bool(string):
    """
    Argument type that takes a case-insensitive string that is
    either "0", "1", "True" or "False".
    """
    
    invalidCount = 0
    validvalues = ["0","1"]
    for v in validvalues:
        if re.match(r'(?i:true)', string) or re.match(r'(?i:false)', string):
            pass
        # TODO: refactor this???
        elif v != string:
            invalidCount = invalidCount.__add__(1)
    if invalidCount == len(validvalues):
        raise ArgumentTypeError("%s is not a valid boolean" % string)
    return string

# PLANNED: "inverted" kwarg which simplifies --destroyallDisabled
# to simply --destroyall, hence the inverted kwarg
def argbool_to_byte(string, *, inverted=False):
    """
    Takes a case-insensitive string that is either "0", "1", "True"
    or "False" and converts it into a byte.

    If inverted is True, returns b'\\x00' and vice versa.
    """
    
    trueMatch = re.match(r'(?i:true)', string)
    falseMatch = re.match(r'(?i:false)', string)
    if trueMatch is not None or string == "1":
        return b'\x01'
    elif falseMatch is not None or string == "0":
        return b'\x00'
    elif trueMatch is None and falseMatch is None:
        raise Exception("strToBool() failed, this shouldn't happen")


def view_values(namespace):
    """
    Parse and print the current values of a Zuma's Revenge! *.dat file.
    """

    values = parse_file(namespace.file)
    print(
        f"File: {values['file']} (version: {values['version']})\n",
        "\n",
        f"start: {values['start']}\n",
        f"repeat: {values['repeat']}\n",
        f"single: {values['single']}\n",
        f"colors: {values['colors']}\n",
        f"speed: {values['speed']}\n",
        f"score: {values['score']}\n",
        "\n",
        f"destroyallDisabled: {values['destroyallDisabled']}\n",
        f"showskull: {values['showskull']}\n",
        f"dieatend: {values['dieatend']}\n",
        f"crashonload: {values['crashonload']}",
    )

def edit_values(namespace):
    """
    Edit the current values of a Zuma's Revenge! *.dat file.
    """

    version = parse_file(namespace.file)["version"]
    datfile = open(namespace.file, "rb+")
    
    original_data = bytes(datfile.read())
    datfile = open(namespace.file, "wb+")
    datfile.write(original_data)

    noneCount = 0
    argvalue = None
    values_dict = vars(namespace)
    for arg in consts.EDIT_OPTIONS:
        if values_dict[arg] is None:
            noneCount = noneCount.__add__(1)
        else:
            datfile.seek(consts.OFFSETS[version][arg])
            if consts.PROPERTY_TYPES[arg] == "int":
                argvalue = values_dict[arg].to_bytes(4, "little")
            elif consts.PROPERTY_TYPES[arg] == "float":
                argvalue = pack('<f',values_dict[arg])
            elif consts.PROPERTY_TYPES[arg] == "bool":
                argvalue = argbool_to_byte(values_dict[arg])
            # elif consts.PROPERTY_TYPES[arg] == "inv_bool":
            #     argvalue = argbool_to_byte(values_dict[arg])
            datfile.write(argvalue)
    if noneCount == consts.EDIT_OPTIONS.__len__():
        raise Exception("No edit options provided.")
    
    datfile.flush()
    datfile.close()