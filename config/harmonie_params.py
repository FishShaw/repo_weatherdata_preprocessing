"""
HARMONIE Model Parameter Mapping Configuration
"""

HARMONIE_PARAMS = {
    1: {'shortName': 'PRES', 'name': 'Pressure', 'units': 'Pa'},
    6: {'shortName': 'GP', 'name': 'Geopotential', 'units': 'm²/s²'},
    11: {'shortName': 'TMP', 'name': 'Temperature', 'units': 'K'},
    20: {'shortName': 'VIS', 'name': 'Visibility', 'units': 'm'},
    33: {'shortName': 'UGRD', 'name': 'U-component of wind', 'units': 'm/s'},
    34: {'shortName': 'VGRD', 'name': 'V-component of wind', 'units': 'm/s'},
    40: {'shortName': 'DZDT', 'name': 'Geometric vertical velocity', 'units': 'm/s'},
    41: {'shortName': 'ABSV', 'name': 'Absolute vorticity', 'units': 's⁻¹'},
    52: {'shortName': 'RH', 'name': 'Relative humidity', 'units': '%'},
    # 65: {'shortName': 'WEASD', 'name': 'Accum. snow', 'units': 'kg/m²'},
    65: {'shortName': 'WEASD', 'name': 'Water equivalent of accumulated snow depth', 'units': 'kg/m²'},
    71: {'shortName': 'TCDC', 'name': 'Total cloud cover', 'units': '%'},
    73: {'shortName': 'LCDC', 'name': 'Low level cloud cover', 'units': '%'},
    74: {'shortName': 'MCDC', 'name': 'Mid level cloud cover', 'units': '%'},
    75: {'shortName': 'HCDC', 'name': 'High level cloud cover', 'units': '%'},
    115: {'shortName': 'LWAVR', 'name': 'Long wave', 'units': 'W/m²'},
    116: {'shortName': 'SWAVR', 'name': 'Short wave', 'units': 'W/m²'},
    117: {'shortName': 'GRAD', 'name': 'Global radiation flux', 'units': 'W/m²'},
    121: {'shortName': 'LHTFL', 'name': 'Latent heat flux', 'units': 'W/m²'},
    122: {'shortName': 'SHTFL', 'name': 'Sensible heat flux', 'units': 'W/m²'},
    160: {'shortName': 'CSUSF', 'name': 'Clear sky upward solar flux', 'units': 'W/m²'},
    161: {'shortName': 'CSDSF', 'name': 'Clear sky downward solar flux', 'units': 'W/m²'},
    162: {'shortName': 'CSULF', 'name': 'Clear sky upward long wave flux', 'units': 'W/m²'},
    163: {'shortName': 'CSDLF', 'name': 'Clear sky downward long wave flux', 'units': 'W/m²'},
    165: {'shortName': 'CFNLF', 'name': 'Cloud forcing net long wave flux', 'units': 'W/m²'},
    181: {'shortName': 'LPSX', 'name': 'Rain', 'units': 'mm'},
    # 181: {'shortName': 'LPSX', 'name': 'x-gradient of log pressure', 'units': '1/m'},
    # 184: {'shortName': 'HGTY', 'name': 'y-gradient of height', 'units': 'm/m'},
    184: {'shortName': 'HGTY', 'name': 'Snow', 'units': 'mm'},
    # 186: {'shortName': 'ICNG', 'name': 'Icing', 'units': 'non-dim'},
    186: {'shortName': 'ICNG', 'name': 'Cloud base', 'units': 'm'},
    187: {'shortName': 'LTNG', 'name': 'Lightning', 'units': 'non-dim'},
    # 201: {'shortName': 'ICWAT', 'name': 'Ice-free water surface', 'units': '%'},
    201: {'shortName': 'ICWAT', 'name': 'Graupel', 'units': 'mm'},
    209: {'shortName': 'MIXLY', 'name': 'No. of mixed layers next to surface', 'units': 'integer'}
}

# Level type mapping
LEVEL_TYPES = {
    '100': 'pl',    # Pressure level
    '103': 'sfc',   # Height above mean sea level
    '105': 'sfc',   # Height above ground
    '200': 'col'    # Entire atmosphere (considered as a single layer)
}

# Common pressure levels (hPa/mb)
PRESSURE_LEVELS = {
    '300': 300,
    '500': 500,
    '600': 600,
    '700': 700,
    '850': 850
}

# Height levels (meters above ground)
HEIGHT_LEVELS = {
    'surface': 0,
    '2m': 2,
    '10m': 10,
    '100m': 100,
    '200m': 200,
    '300m': 300
}

# Time Range Indicator types
TRI_TYPES = {
    0: 'instant',              # Instantaneous value
    2: 'accumulated_limited',  # Accumulated over limited time
    4: 'accumulated_total'     # Total accumulation
}