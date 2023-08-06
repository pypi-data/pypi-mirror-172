from dataclasses import dataclass

ENCODING: str = 'utf-8'

# XXX use this more
link_extract_regex: str = r"(https?://.+?)([ ,\n\\<>]|$)"

@dataclass
class RAW_DATA_FILENAMES():
    BELLINGCAT:     str = 'bellingcat-raw.json'
    CENINFORES:     str = 'ceninfores-raw.json'
    DEFMON:         str = 'defmon-raw.json'
    GEOCONFIRMED:   str = 'geoconfirmed-raw.json'

@dataclass
class SOURCE_NAMES():
    BELLINGCAT:     str = 'BELLINGCAT'
    CENINFORES:     str = 'CENINFORES'
    DEFMON:         str = 'DEFMON'
    GEOCONFIRMED:   str = 'GEOCONFIRMED'
