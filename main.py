import logging
import traceback
import time
from weatherdata_rain_wind import WeatherData
from Pipe import *

class WeatherServer:
    def __init__(self, base_path: str):
        """Initialize weather server with data handler"""
        try:
            logging.info("Initializing WeatherData...")
            self.weather_data = WeatherData(base_path)
            logging.info("WeatherData initialized successfully")
            self.pipe = None
        except Exception as e:
            logging.error(f"Failed to initialize WeatherData: {e}")
            raise

    def start_pipe_server(self):
        """Start the named pipe server"""
        try:
            logging.info("Creating named pipe server...")
            self.pipe = Pipe("KNMI_Interop_", True)
            logging.info("Waiting for client connection...")
            self.pipe.connect()
            logging.info("Client connected successfully")
        except Exception as e:
            logging.error(f"Failed to create/connect pipe: {e}")
            if self.pipe:
                self.pipe.close()
            raise

    def handle_request(self, mid: str, msg: str):
        try:
            if mid == "COORDS":
                lat, lon = map(float, msg.split(','))
                
                # Get weather data for all 16 hours
                all_hours_data = self.weather_data.get_weather_at_coords_all_hours(lat, lon)
                
                # Format response
                response = ""
                for hour in range(16):  # 0-15 hours
                    hour_data = all_hours_data[hour]
                    response += f"{hour}:{hour_data['wind_u']},{hour_data['wind_v']},{hour_data['wind_speed']},{hour_data['rain']}#"
                
                self.pipe.write("WEATHER", response.rstrip('#'))  # Remove trailing #
            else:
                raise Exception("Unknown message id")
                
        except Exception as e:
            self.pipe.write("ERROR", str(e))
            logging.error(traceback.format_exc())

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
        logging.info("Starting Weather Server...")
        server = WeatherServer(base_path)
        logging.info("Weather Server initialized successfully")
        logging.info("Starting pipe server and waiting for connections...")
        server.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error(traceback.format_exc())