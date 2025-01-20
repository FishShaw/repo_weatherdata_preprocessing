import numpy as np
from eccodes import *
from pathlib import Path

class WeatherData:
    def __init__(self, base_path: str):
        """
        Initialize weather data handler for 16-hour forecast
        Args:
            base_path: Path to GRIB files directory
        """
        self.base_path = Path(base_path)
        self.data_cache = {}  # Store data for all hours
        self.max_hours = 16   # Maximum forecast hours
        self.grid_info = None  # Will be initialized when processing first file
        self.data_layers = {}  # Temporary storage for current processing
        
        # 初始化时立即加载第一个小时的数据来设置grid_info
        self._initialize_from_first_file()
        
    def _initialize_from_first_file(self):
        """Initialize grid information from the first available file"""
        first_file = self.base_path / f"fc2024070912+000GB_UWCW01_N20e_selected.grb"
        if not first_file.exists():
            raise FileNotFoundError(f"Initial GRIB file not found: {first_file}")
            
        with open(first_file, 'rb') as f:
            gid = codes_grib_new_from_file(f)
            if gid is None:
                raise ValueError("Could not read initial GRIB message")
            try:
                self._initialize_grid(gid)
            finally:
                codes_release(gid)

    # def get_weather_at_coords_all_hours(self, lat: float, lon: float) -> dict:
    #     """Get 16-hour weather data at specified coordinates"""
    #     if self.grid_info is None:
    #         raise RuntimeError("Grid information not initialized")
            
    #     result = {}
    #     lat_idx, lon_idx = self._find_nearest_indices(lat, lon)
        
    #     for hour in range(self.max_hours):  # Process 0-15 hours
    #         if hour not in self.data_cache:
    #             self._load_hour_data(hour)
            
    #         result[hour] = {
    #             'wind_u': float(self.data_cache[hour]['wind_u'][lat_idx, lon_idx]),
    #             'wind_v': float(self.data_cache[hour]['wind_v'][lat_idx, lon_idx]),
    #             'wind_speed': float(self.data_cache[hour]['wind_speed'][lat_idx, lon_idx]),
    #             'wind_direction': float(self.data_cache[hour]['wind_direction'][lat_idx, lon_idx]), 
    #             'rain': float(self.data_cache[hour]['rain'][lat_idx, lon_idx])
    #         }
    #     return result

    def get_weather_at_coords_list_all_hours(self, coords_list: list) -> dict:
        """Get interpolated 16-hour weather data for a list of coordinates"""
        if self.grid_info is None:
            raise RuntimeError("Grid information not initialized")
        
        result = {}
        
        for hour in range(self.max_hours):
            if hour not in self.data_cache:
                self._load_hour_data(hour)
            
            # 为每个坐标创建数组
            wind_u = np.zeros(len(coords_list))
            wind_v = np.zeros(len(coords_list))
            wind_speed = np.zeros(len(coords_list))
            wind_direction = np.zeros(len(coords_list))
            rain = np.zeros(len(coords_list))
            
            # 对每个坐标进行插值
            for i, (lat, lon) in enumerate(coords_list):
                # 风速等数据使用双线性插值
                wind_u[i] = self._bilinear_interpolation(lat, lon, self.data_cache[hour]['wind_u'])
                wind_v[i] = self._bilinear_interpolation(lat, lon, self.data_cache[hour]['wind_v'])
                wind_speed[i] = self._bilinear_interpolation(lat, lon, self.data_cache[hour]['wind_speed'])
                wind_direction[i] = self._bilinear_interpolation(lat, lon, self.data_cache[hour]['wind_direction'])
                
                # 降雨数据使用最近邻插值
                rain[i] = self._nearest_neighbor_interpolation(lat, lon, self.data_cache[hour]['rain'])
            
            result[hour] = {
                'wind_u': wind_u.tolist(),
                'wind_v': wind_v.tolist(),
                'wind_speed': wind_speed.tolist(),
                'wind_direction': wind_direction.tolist(),
                'rain': rain.tolist()
            }
        
        return result

    def _load_hour_data(self, hour: int):
        """Load data for specific hour"""
        if hour >= self.max_hours:
            raise ValueError(f"Hour {hour} exceeds maximum forecast hours (15)")
            
        current_file = self.base_path / f"fc2024070912+{hour:03d}GB_UWCW01_N20e_selected.grb"
        next_file = self.base_path / f"fc2024070912+{hour+1:03d}GB_UWCW01_N20e_selected.grb"
        
        if not current_file.exists() or not next_file.exists():
            raise FileNotFoundError(f"Required GRIB files not found for hour {hour}")
            
        self.data_cache[hour] = {}
        self._process_wind_data(current_file, hour)
        self._process_rain_data(current_file, next_file, hour)

    def _process_wind_data(self, file_path, hour):
        """Process wind components and calculate wind speed"""
        self.data_layers = {}  # Reset temporary storage
        
        with open(file_path, 'rb') as f:
            while True:
                gid = codes_grib_new_from_file(f)
                if gid is None:
                    break
                    
                try:
                    param_id = codes_get(gid, 'indicatorOfParameter')
                    if self.grid_info is None:
                        self._initialize_grid(gid)
                    
                    values = codes_get_array(gid, 'values')
                    shaped_values = values.reshape(self.grid_info['shape'])
                    
                    if param_id == 33:  # UGRD - 东西方向风速分量
                        self.data_layers['wind_u'] = shaped_values
                    elif param_id == 34:  # VGRD - 南北方向风速分量
                        self.data_layers['wind_v'] = shaped_values
                finally:
                    codes_release(gid)
        
        if 'wind_u' in self.data_layers and 'wind_v' in self.data_layers:
            self.data_layers['wind_speed'] = np.sqrt(
                self.data_layers['wind_u']**2 + 
                self.data_layers['wind_v']**2
            )
            # [新增] 计算风向角度（弧度）
            self.data_layers['wind_direction'] = np.arctan2(
                self.data_layers['wind_v'],
                self.data_layers['wind_u']
            )
            # Store in cache
            self.data_cache[hour]['wind_u'] = self.data_layers['wind_u']
            self.data_cache[hour]['wind_v'] = self.data_layers['wind_v']
            self.data_cache[hour]['wind_speed'] = self.data_layers['wind_speed']
            self.data_cache[hour]['wind_direction'] = self.data_layers['wind_direction']

    def _process_rain_data(self, current_file, next_file, hour):
        """Calculate hourly rainfall from accumulation difference"""
        rain_current = self._get_rain_data(current_file)
        rain_next = self._get_rain_data(next_file)
        
        if rain_current is not None and rain_next is not None:
            rain_diff = rain_next - rain_current
            rain_diff[rain_diff < 0.001] = 0  # Remove negligible negative values
            self.data_cache[hour]['rain'] = rain_diff

    def _get_rain_data(self, file_path):
        """Extract rain data from GRIB file"""
        with open(file_path, 'rb') as f:
            while True:
                gid = codes_grib_new_from_file(f)
                if gid is None:
                    break
                try:
                    param_id = codes_get(gid, 'indicatorOfParameter')
                    indicator = codes_get(gid, 'timeRangeIndicator')
                    if param_id == 181 and indicator == 4:
                        values = codes_get_array(gid, 'values')
                        return values.reshape(self.grid_info['shape'])
                finally:
                    codes_release(gid)
        return None

    def _initialize_grid(self, gid):
        """Initialize grid information"""
        lats = codes_get_array(gid, 'latitudes')
        lons = codes_get_array(gid, 'longitudes')
        nlats = len(np.unique(lats))
        nlons = len(np.unique(lons))
        self.grid_info = {
            'lats': lats.reshape(nlats, nlons),
            'lons': lons.reshape(nlats, nlons),
            'shape': (nlats, nlons)
        }

    # def _find_nearest_indices(self, lat: float, lon: float):
    #     """Find indices of nearest grid point"""
    #     lat_diffs = np.abs(self.grid_info['lats'][:, 0] - lat)
    #     lon_diffs = np.abs(self.grid_info['lons'][0, :] - lon)
    #     return np.argmin(lat_diffs), np.argmin(lon_diffs)
    
    def _bilinear_interpolation(self, lat: float, lon: float, data: np.ndarray) -> float:
        # 找到周围的四个格点
        lat_array = self.grid_info['lats'][:, 0]
        lon_array = self.grid_info['lons'][0, :]
        
        # 找到最近的格点索引
        lat_idx = np.searchsorted(lat_array, lat)
        lon_idx = np.searchsorted(lon_array, lon)
        
        # 确保不超出边界
        if lat_idx == 0:
            lat_idx = 1
        if lon_idx == 0:
            lon_idx = 1
        if lat_idx >= len(lat_array):
            lat_idx = len(lat_array) - 1
        if lon_idx >= len(lon_array):
            lon_idx = len(lon_array) - 1
        
        # 获取四个角点的坐标和值
        lat1, lat2 = lat_array[lat_idx-1], lat_array[lat_idx]
        lon1, lon2 = lon_array[lon_idx-1], lon_array[lon_idx]
        
        q11 = data[lat_idx-1, lon_idx-1]
        q12 = data[lat_idx-1, lon_idx]
        q21 = data[lat_idx, lon_idx-1]
        q22 = data[lat_idx, lon_idx]
        
        # 计算权重
        x = (lon - lon1) / (lon2 - lon1)
        y = (lat - lat1) / (lat2 - lat1)
        
        # 双线性插值公式
        return (q11 * (1-x) * (1-y) +
                q21 * (1-x) * y +
                q12 * x * (1-y) +
                q22 * x * y)

    def _nearest_neighbor_interpolation(self, lat: float, lon: float, data: np.ndarray) -> float:
        """For rain data, use nearest neighbor interpolation"""
        lat_array = self.grid_info['lats'][:, 0]
        lon_array = self.grid_info['lons'][0, :]
        
        # 找到最近的格点索引
        lat_idx = np.abs(lat_array - lat).argmin()
        lon_idx = np.abs(lon_array - lon).argmin()
        
        return float(data[lat_idx, lon_idx])


