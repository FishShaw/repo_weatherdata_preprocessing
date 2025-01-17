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

    def get_weather_at_coords_all_hours(self, lat: float, lon: float) -> dict:
        """Get 16-hour weather data at specified coordinates"""
        if self.grid_info is None:
            raise RuntimeError("Grid information not initialized")
            
        result = {}
        lat_idx, lon_idx = self._find_nearest_indices(lat, lon)
        
        for hour in range(self.max_hours):  # Process 0-15 hours
            if hour not in self.data_cache:
                self._load_hour_data(hour)
            
            result[hour] = {
                'wind_u': float(self.data_cache[hour]['wind_u'][lat_idx, lon_idx]),
                'wind_v': float(self.data_cache[hour]['wind_v'][lat_idx, lon_idx]),
                'wind_speed': float(self.data_cache[hour]['wind_speed'][lat_idx, lon_idx]),
                'rain': float(self.data_cache[hour]['rain'][lat_idx, lon_idx])
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
                    
                    if param_id == 33:  # UGRD
                        self.data_layers['wind_u'] = shaped_values
                    elif param_id == 34:  # VGRD
                        self.data_layers['wind_v'] = shaped_values
                finally:
                    codes_release(gid)
        
        if 'wind_u' in self.data_layers and 'wind_v' in self.data_layers:
            self.data_layers['wind_speed'] = np.sqrt(
                self.data_layers['wind_u']**2 + 
                self.data_layers['wind_v']**2
            )
            # Store in cache
            self.data_cache[hour]['wind_u'] = self.data_layers['wind_u']
            self.data_cache[hour]['wind_v'] = self.data_layers['wind_v']
            self.data_cache[hour]['wind_speed'] = self.data_layers['wind_speed']

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

    def _find_nearest_indices(self, lat: float, lon: float):
        """Find indices of nearest grid point"""
        lat_diffs = np.abs(self.grid_info['lats'][:, 0] - lat)
        lon_diffs = np.abs(self.grid_info['lons'][0, :] - lon)
        return np.argmin(lat_diffs), np.argmin(lon_diffs)