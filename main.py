import logging
import traceback
import time
import json
from weatherdata_rain_wind import WeatherData
from Pipe import *

class WeatherServer:
    def __init__(self, base_path: str):
        """Initialize weather server with data handler"""
        try:
            self.weather_data = WeatherData(base_path)
            self.pipe = None
            self._coord_buffer = []
        except Exception as e:
            logging.error(f"Failed to initialize WeatherData: {e}")
            raise

    def start_pipe_server(self):
        """Start the named pipe server"""
        try:
            self.pipe = Pipe("KNMI_Interop_", True)
            logging.info("Waiting for client connection...")
            self.pipe.connect()
        except Exception as e:
            logging.error(f"Failed to create/connect pipe: {e}")
            if self.pipe:
                self.pipe.close()
            raise

    def handle_request(self, mid: str, msg: str):
        try:
            if mid == "COORDS_CHUNK":
                header, coords = msg.split(":", 1)
                offset, total = map(int, header.split("/"))
                
                chunk_coords = [tuple(map(float, coord.split(","))) 
                              for coord in coords.split("|")]
                
                self._coord_buffer.extend(chunk_coords)
                
                ack_msg = f"{offset}/{total}"
                self.pipe.write("CHUNK_ACK", ack_msg)
                
            elif mid == "COORDS_END":
                coords_list = self._coord_buffer
                weather_data = self.weather_data.get_weather_at_coords_list_all_hours(coords_list)
                
                # 构建JSON格式的响应
                response = {
                    "wind_u": [],
                    "wind_v": [],
                    "wind_speed": [],
                    "wind_direction": [],
                    "rain": []
                }
                
                # 按小时合并数据
                for hour in range(16):
                    hour_data = weather_data[hour]
                    response["wind_u"].extend(hour_data["wind_u"])
                    response["wind_v"].extend(hour_data["wind_v"])
                    response["wind_speed"].extend(hour_data["wind_speed"])
                    response["wind_direction"].extend(hour_data["wind_direction"])
                    response["rain"].extend(hour_data["rain"])
                
                json_response = json.dumps(response)
                self.pipe.write("WEATHER", json_response)
                self._coord_buffer = []
                
            else:
                logging.error(f"Unknown message id: {mid}")
                raise Exception(f"Unknown message id: {mid}")
                
        except Exception as e:
            logging.error(f"Error handling request: {str(e)}")
            logging.error(traceback.format_exc())
            self.pipe.write("ERROR", str(e))

    def run(self):
        """Run the server main loop"""
        while True:
            try:
                if not self.pipe:
                    self.start_pipe_server()
                    continue

                mid, msg = self.pipe.read()
                self.handle_request(mid, msg)
            except Exception as e:
                logging.error(f"Server error: {e}")
                if self.pipe:
                    self.pipe.close()
                    self.pipe = None
                time.sleep(5)  # 等待一段时间后重试


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    base_path = "HARMONIE_AROME_meteo_24hrs/extracted_merged"
    
    try:
        server = WeatherServer(base_path)
        logging.info("Waiting for connections...")
        server.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error(traceback.format_exc())