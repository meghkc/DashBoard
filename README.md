# 🚛 Advanced US Freight Analytics Dashboard

## 🎯 Overview
An interactive, data-driven dashboard for comprehensive analysis of US freight transportation patterns across rail and port modes. This enhanced visualization platform provides deep insights into seasonal trends, performance metrics, and predictive analytics for freight transportation.

## 🚀 Enhanced Features

### ✨ **Professional UI/UX**
- Modern, responsive design with custom CSS styling
- Interactive metric cards and KPI displays
- Mobile-friendly layouts

### 📊 **Advanced Analytics**
- **Multi-Modal Analysis**: Compare rail and port freight transportation
- **Seasonal Decomposition**: Deep dive into seasonal patterns
- **Trend Analysis**: Statistical trend detection with R-squared values
- **Predictive Insights**: Moving averages and anomaly detection
- **Interactive Heatmaps**: Correlation analysis between variables

### 🗺️ **Enhanced Geospatial Visualization**
- Interactive port location maps with volume bubbles
- Regional analysis by coast (Atlantic, Pacific, Gulf)
- Geographic performance distribution

### 📈 **Advanced Chart Types**
- Sunburst charts for hierarchical data
- Interactive heatmaps with hover details
- Time series with statistical trend lines
- Growth rate analysis with year-over-year comparisons
- Capacity utilization indicators

### 🔍 **Data Intelligence**
- Automated anomaly detection
- Statistical insights and summaries
- Performance benchmarking
- Custom filtering and cross-filtering

## 📂 Project Structure

```
DashBoard/
├── 📱 streamlit_app.py          # Main dashboard application (Streamlit Cloud ready)
├── 📋 requirements.txt          # Python dependencies 
├── 📖 README.md                 # Project documentation
├── 📜 LICENSE                   # MIT License
├── 🔧 .gitignore               # Git ignore rules
├── 🛠️ setup.py                 # Automated setup script
├── 📝 CHANGELOG.md             # Version history and updates
├── 🤝 CONTRIBUTING.md          # Contribution guidelines  
├── 🔐 SECURITY.md              # Security policy and reporting
├── 🚀 run_dashboard.bat        # Windows launcher script
├── 📊 Data/                    # Dataset files
│   ├── Rail_Carloadings_originated.csv    # Rail freight data (124K+ records)
│   └── port_dataset.json                  # Port container data (78 records)
├── 📁 Script/                  # Development and legacy versions
│   ├── enhanced_dashboard.py              # Enhanced development version
│   ├── dash_water_rail.py                # Original dashboard  
│   └── test_dashboard.py                 # Testing utilities
├── ⚙️ .vscode/                 # VS Code configuration
├── 🐳 .devcontainer/          # Development container setup
└── 🔄 .github/                # GitHub Actions and templates
    ├── workflows/
    │   └── ci.yml              # Continuous Integration
    └── ISSUE_TEMPLATE/
        ├── bug_report.yml      # Bug report template
        └── feature_request.yml # Feature request template
```

## 🎨 Dashboard Sections

### 1. **🚆 Rail Analytics**
- **Overview**: Trend analysis with statistical insights, interactive heatmaps
- **Seasonal Analysis**: Sunburst charts, year-over-year seasonal comparisons
- **Trend Analysis**: Growth rate calculations, performance tracking
- **Predictive Insights**: Moving averages, anomaly detection

### 2. **🚢 Port Analytics**
- **Overview**: Interactive maps, time series comparisons
- **Performance Metrics**: Capacity utilization, regional analysis
- **Seasonal Patterns**: Coast-based seasonal analysis
- **Growth Analysis**: Port ranking and performance trends

### 3. **📊 Comparative Analysis**
- **Multi-Modal Comparison**: Rail vs Port volume analysis
- **Market Share Evolution**: Modal share tracking over time
- **Conversion Analytics**: TEU equivalent calculations
- **Strategic Insights**: Mode-specific advantages analysis

## 🛠️ Technical Features

### **Performance Optimizations**
- `@st.cache_data` for efficient data loading
- Progressive loading for large datasets

### **Advanced Libraries**
- **Plotly**: Interactive charts with hover details
- **SciPy**: Statistical analysis and trend detection
- **Pandas**
- **NumPy**

### **Professional Styling**
- Custom CSS with gradient backgrounds
- Responsive metric cards
- Color-coded insights and alerts

## 🚀 Quick Start

### 🌐 **Live Demo**
**[View Live Dashboard on Streamlit Cloud](https://share.streamlit.io/meghkc/dashboard)** 🔗

### **Option 1: Automated Setup (Recommended)**
```bash
# Clone the repository
git clone https://github.com/meghkc/DashBoard.git
cd DashBoard

# Run automated setup
python setup.py

# Launch dashboard (auto-generated launcher)
# Windows: launch_dashboard.bat
# Linux/Mac: ./launch_dashboard.sh
```

### **Option 2: Easy Launch (Windows)**
```bash
# Double-click the launcher
run_dashboard.bat
```

### **Option 3: Manual Setup**
```bash
# Clone and navigate
git clone https://github.com/meghkc/DashBoard.git
cd DashBoard

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the main dashboard (Streamlit Cloud compatible)
streamlit run streamlit_app.py
```

### **☁️ Cloud Deployment**
- **Streamlit Cloud**: Fork repo → Connect GitHub → Deploy
- **Heroku/Railway/Render**: Direct deployment support
- **Docker**: `docker build -t freight-dashboard .`

```

## 📊 Data Sources & Specifications

### **Rail Dataset**
- **Source**: USDA Agricultural Transportation
- **Records**: 124,293 entries
- **Timespan**: 2017-2023 (7 years)
- **Granularity**: Weekly data
- **Key Metrics**: Carloads by railroad, commodity, and time

### **Port Dataset**
- **Source**: Individual port authority websites
- **Records**: 78 monthly entries
- **Coverage**: 9 major US container ports
- **Timespan**: 2018-2024
- **Key Metrics**: TEU (Twenty-foot Equivalent Units)

## 🎯 Analytics Features

### **KPI Dashboard**
- Total freight volume metrics
- Growth rate calculations
- Peak performance indicators
- Operational efficiency metrics

### **Data Insights**
- Anomaly detection alerts
- Seasonal pattern recognition
- Performance benchmarking
- Trend significance testing

### **Export Capabilities**
- Data download options
- Chart export functionality
- Report generation ready

## 👨‍💻 Technical Specifications

### **System Requirements**
- Python 3.8+
- 4GB RAM minimum
- Modern web browser
- Internet connection for maps

### **Dependencies**

streamlit >= 1.48.0
pandas >= 1.5.0
plotly >= 5.0.0
scipy >= 1.9.0
scikit-learn >= 1.1.0
seaborn >= 0.11.0
numpy >= 1.21.0


## 📈 Performance Metrics

### **Dashboard Load Time**: < 3 seconds
### **Data Processing**: Cached for optimal performance
### **Responsiveness**: Mobile and desktop optimized
### **Scalability**: Handles 100K+ records efficiently


## 🔗 Links & Resources

- **Data Source (Rail)**: [USDA Agricultural Transportation](https://agtransport.usda.gov/stories/s/appm-bhti)
- **Data Source (Ports)**: Individual port authority websites
- **Framework**: Built with Streamlit
- **Visualization**: Powered by Plotly
- **Author**: Megh KC | Created 2024 | Enhanced 2025

---
