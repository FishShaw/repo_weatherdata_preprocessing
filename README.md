# 🌦️ Weather Digital Twin - Data Processing Engine

## Real-time Meteorological Data Pipeline | Master's Thesis Project | Wageningen University

Powering the next generation of interactive climate visualization through advanced data processing, spatial interpolation, and real-time system integration.

![Interpolation Results](Docs/Image/interpolation_result_1.png)

## 🎯 Project Overview

This repository contains the **data processing backbone** of an interactive weather digital twin system - a sophisticated pipeline that transforms raw meteorological forecasts into real-time 3D experiences. The system demonstrates advanced capabilities in **large-scale data processing**, **real-time system integration**, and **spatial analysis validation**.

### 🔬 Technical Challenge Solved

**The Problem**: Bridge the gap between complex meteorological GRIB datasets and real-time Unity 3D visualization, requiring sub-second response times and spatial accuracy across multiple interpolation methods.

**The Solution**: An end-to-end data processing pipeline that handles KNMI HARMONIE-AROME weather forecasts, performs real-time spatial interpolation, and maintains live communication with Unity through custom-built IPC systems.

## 🚀 Core Technical Achievements

### 🏗️ **Complex System Integration**
- **Multi-format Data Pipeline**: GRIB → Python → Unity → 3D Visualization
- **Real-time Communication**: Custom Windows Named Pipe implementation for sub-second data streaming
- **Cross-platform Coordination**: Seamless Python-Unity integration with error handling and data validation

### 📊 **Advanced Spatial Data Processing**
- **Multi-method Interpolation Engine**: Implemented and benchmarked 5 spatial interpolation algorithms
- **Geospatial Accuracy**: Maintained precision across coordinate transformations (WGS84 ↔ RD ↔ Grid coordinates)
- **Performance Optimization**: Efficient processing of 390×390 weather grids covering the Netherlands

### 🔬 **Comprehensive Validation Framework**
- **Statistical Analysis**: RMSE, MAE, R², Nash-Sutcliffe efficiency comparisons
- **Temporal Consistency**: 16-hour forecast validation across multiple weather parameters
- **Spatial Correlation**: Cross-validation across different geographical locations

## 🛠️ System Architecture

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   KNMI GRIB     │    │   Python Data   │    │  Unity 3D Scene │
│   Weather Data  │───▶│   Processing    │───▶│   Visualization │
│                 │    │   Engine        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        │              ┌─────────────────┐              │
        │              │  Interpolation  │              │
        └──────────────│   Validation    │──────────────┘
                       │    Framework    │
                       └─────────────────┘
```

### **Data Flow Pipeline**

1. **🌐 Data Acquisition**: HARMONIE-AROME GRIB files (24h forecasts, 2.5km resolution)
2. **🔧 Preprocessing**: GRIB decoding, coordinate transformation, data validation  
3. **🧮 Spatial Interpolation**: Real-time processing using multiple algorithms
4. **📡 Real-time Streaming**: Windows Named Pipe communication to Unity
5. **🎮 3D Rendering**: Live weather visualization in interactive environment

## 📈 Performance Results

### **Interpolation Method Comparison**

![Interpolation Performance](Docs/Image/interpolation_result_2.png)

**Key Findings:**
- **Bilinear**: Best balance of accuracy and performance (RMSE: 0.0065 for wind data)
- **RBF**: Superior for complex terrain (RMSE: 0.0349)
- **Kriging**: Excellent for rainfall prediction (R² > 0.99)

### **System Performance Metrics**

- **Data Processing Speed**: < 100ms per weather grid
- **Real-time Communication**: < 50ms latency Unity-Python
- **Memory Efficiency**: 390×390 grids processed in < 2GB RAM
- **Accuracy**: 95%+ correlation with ground truth across all parameters

## 🔧 Technical Implementation

### **Core Components**

#### 1. **Data Processing Engine** (`weatherdata_rain_wind.py`)
```python
# Advanced spatial interpolation with multiple algorithms
class WeatherData:
    def get_weather_at_coords_list_all_hours(self, coords_list: list) -> dict:
        # Bilinear, IDW, Kriging, Spline, RBF implementations
        # Real-time coordinate transformation and validation
```

#### 2. **Real-time Communication** (`Pipe.py`)
```python
# Custom Windows Named Pipe for Unity-Python IPC
class Pipe:
    def write(self, message_id: str, content: str):
        # High-performance data streaming with error handling
```

#### 3. **System Integration** (`main.py`)
```python
# Weather server orchestrating the entire pipeline
class WeatherServer:
    def process_unity_request(self, coordinates: list) -> dict:
        # End-to-end request processing and response generation
```

### **Advanced Features**

- **🔄 Adaptive Interpolation**: Method selection based on parameter type and spatial distribution
- **⚡ Caching System**: Intelligent data caching for improved performance
- **🛡️ Error Recovery**: Robust error handling with fallback mechanisms
- **📊 Real-time Monitoring**: Performance metrics and system health tracking

## 📊 Validation & Analysis

### **Comprehensive Testing Framework**

The system includes extensive validation notebooks demonstrating:

#### **Spatial Interpolation Analysis** (`weatherdata_stat.ipynb`)
- Cross-validation across multiple Dutch cities (Wageningen, Groningen, Tilburg)
- Temporal consistency analysis over 16-hour forecasts
- Statistical significance testing and confidence interval analysis

#### **Visual Analytics** (`timeseries_visualization_rain.ipynb`)
- Interactive time-series visualization
- Spatial correlation mapping
- Real-time data quality assessment

#### **Performance Benchmarking** (`Harmonie_for_unitydata.ipynb`)
- System load testing
- Memory usage optimization
- Communication latency measurement

## 📁 Repository Structure

```text
📦 Weather Data Processing Engine
├── 🔧 Core Processing
│   ├── weatherdata_rain_wind.py    # Main data processing engine
│   ├── main.py                     # System orchestration
│   └── Pipe.py                     # Unity communication
├── 📊 Analysis & Validation
│   ├── weatherdata_stat.ipynb      # Statistical analysis
│   ├── timeseries_visualization_rain.ipynb
│   └── Harmonie_for_unitydata.ipynb
├── 🗄️ Data Management
│   ├── HARMONIE_AROME_meteo_24hrs/  # Weather datasets
│   ├── interpolation_stat/         # Validation results
│   └── coordinates_storage/        # Spatial reference data
├── 🛠️ Utilities
│   ├── utils/                      # Helper functions
│   ├── config/                     # Configuration files
│   └── Docs/                       # Documentation and images
└── 🎮 Unity Assets
    ├── unity_textures/             # Weather visualization textures
    └── wind_fields/                # Vector field data
```

---

