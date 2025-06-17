from camel_tools.utils.normalize import normalize_alef_ar as alef
from camel_tools.utils.normalize import normalize_alef_maksura_ar as yeh
from camel_tools.utils.normalize import normalize_teh_marbuta_ar as teh


def normalize_alef_yeh_ta_line(line):
    return alef(yeh(teh(line)))

def normalize_alef_yeh_ta(lines):
    return [normalize_alef_yeh_ta_line(line) for line in lines]