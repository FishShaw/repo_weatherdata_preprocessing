# """
# Parameter mapping utilities for GRIB data processing
# 其中得map_parameter函数用于将GRIB消息中的参数信息映射到配置文件中的参数信息(重要！！！)
# """

# from typing import Dict, Any, Optional, Union
# from config.harmonie_params import (
#     HARMONIE_PARAMS,
#     LEVEL_TYPES,
#     PRESSURE_LEVELS,
#     HEIGHT_LEVELS,
#     TRI_TYPES
# )

# class ParameterMapper:
#     """
#     Class to handle parameter mapping for GRIB data
#     """
    
#     @staticmethod
#     def map_parameter(grib_id: int) -> Dict[str, Any]:
#         """
#         Map GRIB parameter information using configuration
#         使用配置映射GRIB参数信息

#         Args:
#             grib_id: GRIB message ID from eccodes

#         Returns:
#             Dict containing mapped parameter information
#         """
#         import eccodes
        
#         try:
#             # Get basic parameter information
#             param_code = eccodes.codes_get(grib_id, 'indicatorOfParameter')
#             level_type = str(eccodes.codes_get(grib_id, 'indicatorOfTypeOfLevel'))
#             level = eccodes.codes_get(grib_id, 'level')
#             tri = eccodes.codes_get(grib_id, 'timeRangeIndicator', None)

#             # Get parameter information from mapping
#             param_info = HARMONIE_PARAMS.get(param_code, {
#                 'shortName': 'unknown',
#                 'name': f'Unknown Parameter ({param_code})',
#                 'units': 'unknown'
#             })

#             # Map level type
#             mapped_level_type = LEVEL_TYPES.get(level_type, 'unknown')

#             # Create mapped information dictionary
#             mapped_info = {
#                 'parameter': {
#                     'code': param_code,
#                     'shortName': param_info['shortName'],
#                     'name': param_info['name'],
#                     'units': param_info['units']
#                 },
#                 'level': {
#                     'type': mapped_level_type,
#                     'value': level,
#                     'original_type': level_type
#                 }
#             }

#             # Add time range indicator if present
#             if tri is not None:
#                 mapped_info['timeRange'] = {
#                     'indicator': tri,
#                     'type': TRI_TYPES.get(tri, 'unknown')
#                 }

#             return mapped_info

#         except Exception as e:
#             print(f"Error mapping parameter: {e}")
#             return {}

#     @staticmethod
#     def get_grib_data(grib_id: int) -> Dict[str, Any]:
#         """
#         Get complete mapped data from GRIB message
#         从GRIB消息获取完整的映射数据，尤其是经纬度数据和值数据

#         Args:
#             grib_id: GRIB message ID from eccodes

#         Returns:
#             Dict containing all mapped data and values
#         """
#         import eccodes
#         import numpy as np

#         try:
#             # Get mapped parameter information
#             mapped_info = ParameterMapper.map_parameter(grib_id)
            
#             # Get geographical information and values
#             lats = eccodes.codes_get_array(grib_id, 'latitudes')
#             lons = eccodes.codes_get_array(grib_id, 'longitudes')
#             values = eccodes.codes_get_array(grib_id, 'values')

#             # Get grid dimensions
#             nlats = len(np.unique(lats))
#             nlons = len(np.unique(lons))

#             # Add data arrays to mapped information
#             mapped_info['data'] = {
#                 'lats': lats.reshape(nlats, nlons),
#                 'lons': lons.reshape(nlats, nlons),
#                 'values': values.reshape(nlats, nlons)
#             }

#             # Add grid information
#             mapped_info['grid'] = {
#                 'nx': nlons,
#                 'ny': nlats,
#                 'resolution': {
#                     'lat': abs(lats[1] - lats[0]),
#                     'lon': abs(lons[1] - lons[0])
#                 }
#             }

#             return mapped_info

#         except Exception as e:
#             print(f"Error getting GRIB data: {e}")
#             return {}

#     @staticmethod
#     def print_parameter_info(mapped_info: Dict[str, Any]) -> None:
#         """
#         Print formatted parameter information
#         打印格式化的参数信息

#         Args:
#             mapped_info: Mapped parameter information
#         """
#         if not mapped_info:
#             print("No parameter information available")
#             return

#         print("\nParameter Information:")
#         print(f"  Name: {mapped_info['parameter']['name']}")
#         print(f"  Short Name: {mapped_info['parameter']['shortName']}")
#         print(f"  Code: {mapped_info['parameter']['code']}")
#         print(f"  Units: {mapped_info['parameter']['units']}")
#         print(f"  Level: {mapped_info['level']['value']} ({mapped_info['level']['type']})")
        
#         if 'timeRange' in mapped_info:
#             print(f"  Time Range: {mapped_info['timeRange']['type']}")

#         if 'grid' in mapped_info:
#             print("\nGrid Information:")
#             print(f"  Dimensions: {mapped_info['grid']['nx']} x {mapped_info['grid']['ny']}")
#             print(f"  Resolution: {mapped_info['grid']['resolution']['lat']}° x "
#                   f"{mapped_info['grid']['resolution']['lon']}°")



"""
Parameter mapping utilities for GRIB data processing
GRIB数据处理的参数映射工具

主要功能：
1. 参数映射：将GRIB消息中的参数信息映射到配置文件中的参数信息
2. 数据提取：获取GRIB消息中的完整数据（包括地理信息和值）
3. 文件读取：读取GRIB文件中的所有消息
4. 参数查找：在映射数据中查找特定参数
5. 信息打印：格式化打印参数信息
"""

from typing import Dict, Any, Optional, Union, List
from config.harmonie_params import (
    HARMONIE_PARAMS,
    LEVEL_TYPES,
    PRESSURE_LEVELS,
    HEIGHT_LEVELS,
    TRI_TYPES
)
import os
import eccodes
import numpy as np

class ParameterMapper:
    """
    Class to handle parameter mapping and data extraction for GRIB data
    处理GRIB数据的参数映射和数据提取的类
    
    主要方法：
    - map_parameter: 映射单个GRIB消息的参数信息
    - get_grib_data: 获取单个GRIB消息的完整数据
    - read_grib_file: 读取整个GRIB文件的所有消息
    - find_parameter: 在映射数据中查找特定参数
    - print_parameter_info: 打印参数信息
    """
    
    @staticmethod
    def map_parameter(grib_id: int) -> Dict[str, Any]:
        """
        Map GRIB parameter information using configuration
        使用配置映射GRIB参数信息
        
        功能：将GRIB消息中的基本参数信息映射到配置文件中定义的参数信息
        
        Args:
            grib_id: GRIB message ID from eccodes

        Returns:
            Dict containing mapped parameter information
        """
        try:
            # Get basic parameter information
            param_code = eccodes.codes_get(grib_id, 'indicatorOfParameter')
            level_type = str(eccodes.codes_get(grib_id, 'indicatorOfTypeOfLevel'))
            level = eccodes.codes_get(grib_id, 'level')
            tri = eccodes.codes_get(grib_id, 'timeRangeIndicator', None)

            # Get parameter information from mapping
            param_info = HARMONIE_PARAMS.get(param_code, {
                'shortName': 'unknown',
                'name': f'Unknown Parameter ({param_code})',
                'units': 'unknown'
            })

            # Map level type
            mapped_level_type = LEVEL_TYPES.get(level_type, 'unknown')

            # Create mapped information dictionary
            mapped_info = {
                'parameter': {
                    'code': param_code,
                    'shortName': param_info['shortName'],
                    'name': param_info['name'],
                    'units': param_info['units']
                },
                'level': {
                    'type': mapped_level_type,
                    'value': level,
                    'original_type': level_type
                }
            }

            # Add time range indicator if present
            if tri is not None:
                mapped_info['timeRange'] = {
                    'indicator': tri,
                    'type': TRI_TYPES.get(tri, 'unknown')
                }

            return mapped_info

        except Exception as e:
            print(f"Error mapping parameter: {e}")
            return {}

    @staticmethod
    def get_grib_data(grib_id: int) -> Dict[str, Any]:
        """
        Get complete mapped data from GRIB message
        从GRIB消息获取完整的映射数据
        
        功能：
        1. 获取参数映射信息
        2. 提取地理数据（经纬度）
        3. 提取值数据
        4. 添加网格信息
        
        Args:
            grib_id: GRIB message ID from eccodes

        Returns:
            Dict containing all mapped data and values
        """
        try:
            # Get mapped parameter information
            mapped_info = ParameterMapper.map_parameter(grib_id)
            
            # Get geographical information and values
            lats = eccodes.codes_get_array(grib_id, 'latitudes')
            lons = eccodes.codes_get_array(grib_id, 'longitudes')
            values = eccodes.codes_get_array(grib_id, 'values')

            # Get grid dimensions
            nlats = len(np.unique(lats))
            nlons = len(np.unique(lons))

            # Add data arrays to mapped information
            mapped_info['data'] = {
                'lats': lats.reshape(nlats, nlons),
                'lons': lons.reshape(nlats, nlons),
                'values': values.reshape(nlats, nlons)
            }

            # Add grid information
            mapped_info['grid'] = {
                'nx': nlons,
                'ny': nlats,
                'resolution': {
                    'lat': abs(lats[1] - lats[0]),
                    'lon': abs(lons[1] - lons[0])
                }
            }

            return mapped_info

        except Exception as e:
            print(f"Error getting GRIB data: {e}")
            return {}

    @staticmethod
    def read_grib_file(filepath: str) -> List[Dict[str, Any]]:
        """
        Read all messages from a GRIB file
        读取GRIB文件中的所有消息
        
        功能：
        1. 打开并读取GRIB文件
        2. 处理文件中的每个消息
        3. 获取每个消息的完整映射数据
        4. 返回所有消息的数据列表
        
        Args:
            filepath: Path to the GRIB file

        Returns:
            List of dictionaries containing mapped data for each message
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
            
        data = []
        with open(filepath, 'rb') as f:
            while True:
                gid = eccodes.codes_grib_new_from_file(f)
                if gid is None:
                    break
                
                try:
                    mapped_data = ParameterMapper.get_grib_data(gid)
                    if mapped_data:
                        ParameterMapper.print_parameter_info(mapped_data)
                        data.append(mapped_data)
                    
                except Exception as e:
                    print(f"Error reading message: {e}")
                finally:
                    eccodes.codes_release(gid)
        
        return data

    @staticmethod
    def find_parameter(data: List[Dict[str, Any]], short_name: str) -> Dict[str, Any]:
        """
        Find specific parameter in mapped data
        在映射数据中查找特定参数
        
        功能：
        1. 在数据列表中查找指定短名称的参数
        2. 如果未找到，显示可用参数列表
        
        Args:
            data: List of mapped parameter data
            short_name: Short name of the parameter to find

        Returns:
            Dictionary containing the found parameter data
            
        Raises:
            StopIteration: If parameter not found
        """
        try:
            return next(d for d in data if d['parameter']['shortName'] == short_name)
        except StopIteration:
            print(f"\nError: Parameter '{short_name}' not found in data!")
            print("Available parameters:")
            for d in data:
                print(f"- {d['parameter']['shortName']} ({d['parameter']['name']})")
            raise

    @staticmethod
    def print_parameter_info(mapped_info: Dict[str, Any]) -> None:
        """
        Print formatted parameter information
        打印格式化的参数信息
        
        功能：
        1. 打印参数基本信息（名称、单位等）
        2. 打印层级信息
        3. 打印时间范围信息（如果有）
        4. 打印网格信息（如果有）
        
        Args:
            mapped_info: Mapped parameter information
        """
        if not mapped_info:
            print("No parameter information available")
            return

        print("\nParameter Information:")
        print(f"  Name: {mapped_info['parameter']['name']}")
        print(f"  Short Name: {mapped_info['parameter']['shortName']}")
        print(f"  Code: {mapped_info['parameter']['code']}")
        print(f"  Units: {mapped_info['parameter']['units']}")
        print(f"  Level: {mapped_info['level']['value']} ({mapped_info['level']['type']})")
        
        if 'timeRange' in mapped_info:
            print(f"  Time Range: {mapped_info['timeRange']['type']}")

        if 'grid' in mapped_info:
            print("\nGrid Information:")
            print(f"  Dimensions: {mapped_info['grid']['nx']} x {mapped_info['grid']['ny']}")
            print(f"  Resolution: {mapped_info['grid']['resolution']['lat']}° x "
                  f"{mapped_info['grid']['resolution']['lon']}°")