"""
GRIB File Processing Utilities
"""
import os
import eccodes
from typing import Dict, List, Any
from config.harmonie_params import (
    HARMONIE_PARAMS,
    LEVEL_TYPES,
    PRESSURE_LEVELS,
    HEIGHT_LEVELS,
    TRI_TYPES,
)

def extract_and_merge_layers(
    input_path: str, 
    output_path: str, 
    layers_to_extract: List[Dict[str, Any]]
) -> None:
    """
    Args:
        input_path (str): Path to input GRIB file
        output_path (str): Path for output GRIB file
        layers_to_extract (List[Dict]): List of layer specifications to extract
    """
    print(f"Processing file: {input_path}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    selected_messages = []

    with open(input_path, 'rb') as f:
        while True:
            # Read GRIB message
            gid = eccodes.codes_grib_new_from_file(f)
            if gid is None:
                break
            try:
                # Get message identifiers
                param_code = eccodes.codes_get(gid, 'indicatorOfParameter')
                level_type = eccodes.codes_get(gid, 'indicatorOfTypeOfLevel')
                level = eccodes.codes_get(gid, 'level')
                tri = eccodes.codes_get(gid, 'timeRangeIndicator', None)
                
                # Get parameter information from mapping
                param_info = HARMONIE_PARAMS.get(param_code, {
                    'shortName': 'unknown',
                    'name': 'unknown',
                    'units': 'unknown'
                })

                # Get short name and handle special cases
                short_name = param_info['shortName']
                
                # Standardize level type using mapping
                level_type_str = LEVEL_TYPES.get(str(level_type), str(level_type))
                
                # Check each layer specification for matches
                for layer in layers_to_extract:
                    if _check_layer_match(layer, param_code, short_name, level, level_type_str, tri):
                        clone_id = eccodes.codes_clone(gid)
                        selected_messages.append(clone_id)
                        _print_match_info(short_name, param_code, level, level_type_str, tri)
                        break
                
            except Exception as e:
                print(f"Error processing message: {e}")
            finally:
                eccodes.codes_release(gid)
    
    _write_selected_messages(selected_messages, output_path, len(layers_to_extract))

def _check_layer_match(
    layer: Dict[str, Any],
    param_code: int,
    short_name: str,
    level: int,
    level_type: str,
    tri: int
) -> bool:
    """
    Check if a layer matches the specified criteria
    
    Args:
        layer (Dict): Layer specification to match against
        param_code (int): Parameter code
        short_name (str): Parameter short name
        level (int): Level value
        level_type (str): Level type
        tri (int): Time Range Indicator
    
    Returns:
        bool: True if layer matches all criteria, False otherwise
    """
    matches = True
    
    # Check short name match
    if 'shortName' in layer and layer['shortName'] != short_name:
        matches = False
    # Check parameter number match
    if 'parameterNumber' in layer and layer['parameterNumber'] != param_code:
        matches = False
    # Check level value match
    if 'level' in layer and layer['level'] != level:
        matches = False
    # Check level type match
    if 'levelType' in layer and layer['levelType'] != level_type:
        matches = False
    # Check time range indicator match
    if 'tri' in layer and tri is not None and layer['tri'] != tri:
        matches = False
    
    return matches

def _print_match_info(
    short_name: str,
    param_code: int,
    level: int,
    level_type: str,
    tri: int = None
) -> None:
    """
    Print information about matched layer
    
    Args:
        short_name (str): Parameter short name
        param_code (int): Parameter code
        level (int): Level value
        level_type (str): Level type
        tri (int, optional): Time Range Indicator
    """
    print(f"\nFound matching message:")
    print(f"  Parameter: {short_name} (code: {param_code})")
    print(f"  Level: {level} {level_type}")
    if tri is not None:
        print(f"  TRI: {tri} ({TRI_TYPES.get(tri, 'unknown')})")

def _write_selected_messages(
    messages: List[int],
    output_path: str,
    total_layers: int
) -> None:
    """
    Write selected messages to output GRIB file
    
    Args:
        messages (List[int]): List of message IDs to write
        output_path (str): Path to output file
        total_layers (int): Total number of layers requested
    """
    if messages:
        with open(output_path, 'wb') as out:
            for msg_id in messages:
                eccodes.codes_write(msg_id, out)
                eccodes.codes_release(msg_id)
        print(f"\nCreated: {output_path}")
        print(f"Selected {len(messages)} of {total_layers} layers")
    else:
        print(f"\nWarning: Found 0 of {total_layers} layers")

