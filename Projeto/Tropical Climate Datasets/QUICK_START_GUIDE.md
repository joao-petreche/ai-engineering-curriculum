# 🚀 QUICK START GUIDE: Tropical Building Energy Datasets

## Top 3 Recommendations for Your Requirements

### 🥇 #1: Building Data Genome Project 2 (BDG2)
**Why:** Largest, immediately available, proven ML benchmark, includes some tropical sites

**Quick Access:**
```bash
git clone https://github.com/buds-lab/building-data-genome-project-2.git
cd building-data-genome-project-2
# Data is in data/meters/raw/
# Weather data in data/weather/
# Metadata in data/metadata/
```

**What you get:**
- 3,053 meters from 1,636 buildings
- Hourly data for 2 full years (2016-2017)
- ~53.6 million measurements
- Electricity, heating/cooling, weather data
- Ready for ML (used in Kaggle competition)

**Documentation:** https://www.nature.com/articles/s41597-020-00712-x

---

### 🥈 #2: Singapore Sub-hourly Dataset (6 Buildings)
**Why:** 100% tropical climate, sub-hourly resolution, real IoT sensors

**Quick Access:**
1. Visit Nature Scientific Data: https://www.nature.com/sdata/
2. Search: "Sub-hourly measurement datasets 6 real buildings Singapore"
3. Or use DOI: **10.1038/s41597-023-02525-3**
4. Download from linked repository (usually Figshare)

**What you get:**
- 6 operational buildings in Singapore tropical climate
- Sub-hourly measurements (15-min to 1-hour)
- Energy, temperature, humidity, HVAC, weather
- Multi-year monitoring
- Perfect for addressing "reality gap"

---

### 🥉 #3: I-BLEND (India Campus Dataset)
**Why:** 100% hot-humid Indian climate, designed for ML, campus-scale

**Quick Access:**
1. Visit Nature Scientific Data: https://www.nature.com/sdata/
2. Search: "I-BLEND India building energy dataset"
3. Or use DOI: **10.1038/s41597-022-01721-4**
4. Download from linked repository

**What you get:**
- Campus-scale commercial and residential buildings
- Sub-hourly to hourly measurements
- Energy, HVAC, temperature, humidity, occupancy
- Indian hot-humid and composite climate zones
- Specifically designed for ML applications

---

## Additional Tropical Datasets

### 🌴 Ecuador Commercial Buildings (Very Hot Humid)
**Access:** https://www.mdpi.com/2071-1050/16/22/9770
- Check "Supplementary Materials" section
- Or contact authors for data access
- Hourly smart meter data from Ecuadorian coast
- 5 months of data from public/commercial buildings

### 🌴 Tropical Courtyard Buildings Dataset
**Access:** https://www.sciencedirect.com/science/article/pii/S235234092500561X
- Open access on ScienceDirect
- Field measurements from tropical climate
- Energy, temperature, humidity, WBGT, MRT
- Good for validation studies

---

## Step-by-Step Access Instructions

### For Immediate Start (Today):

**Step 1:** Download BDG2
```bash
# In your terminal
cd ~/Documents  # or your preferred directory
git clone https://github.com/buds-lab/building-data-genome-project-2.git
cd building-data-genome-project-2

# Explore the data
ls data/meters/raw/          # Energy meter data
ls data/weather/             # Weather data
ls data/metadata/            # Building metadata
ls notebooks/                # Example Jupyter notebooks
```

**Step 2:** Explore BDG2 Data Structure
```python
import pandas as pd

# Load a sample meter file
meter_data = pd.read_csv('data/meters/raw/electricity_0.csv')
print(meter_data.head())

# Load building metadata
metadata = pd.read_csv('data/metadata/metadata.csv')
print(metadata.head())

# Load weather data
weather = pd.read_csv('data/weather/weather.csv')
print(weather.head())
```

### For Tropical-Specific Data (This Week):

**Step 1:** Access Singapore Dataset
1. Go to: https://www.nature.com/sdata/
2. Search: "Singapore sub-hourly building measurements"
3. Click on the 2023 paper
4. Look for "Data Availability" section
5. Download from linked repository (Figshare or Zenodo)

**Step 2:** Access I-BLEND Dataset
1. Go to: https://www.nature.com/sdata/
2. Search: "I-BLEND India building energy"
3. Click on the 2022 paper
4. Look for "Data Availability" section
5. Download from linked repository

**Step 3:** Access Ecuador Dataset
1. Go to: https://www.mdpi.com/2071-1050/16/22/9770
2. Scroll to "Supplementary Materials"
3. Download available data files
4. If not available, click "Request Data" or contact authors

---

## Dataset Comparison at a Glance

| Feature | BDG2 | Singapore 6 | I-BLEND | Ecuador |
|---------|------|-------------|---------|---------|
| **Tropical Focus** | Partial | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Scale** | 1,636 bldgs | 6 buildings | Campus | Multiple |
| **Frequency** | Hourly | Sub-hourly | Sub-hourly | Hourly |
| **Duration** | 2 years | Multi-year | Multi-year | 5 months |
| **ML Ready** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Access** | Immediate | Register | Register | Check paper |
| **Reality Gap** | Real meters | Real IoT | Real IoT | Real meters |

---

## What Each Dataset Provides

### Energy Metrics:
✅ **All datasets:** Whole building electricity  
✅ **BDG2, Singapore, I-BLEND:** HVAC energy (heating/cooling)  
✅ **BDG2:** Steam, irrigation, solar  

### IEQ Variables:
✅ **All datasets:** Indoor temperature  
✅ **All datasets:** Relative humidity  
✅ **Singapore, I-BLEND:** Detailed HVAC operation  
✅ **Tropical courtyard:** Mean Radiant Temperature, WBGT  

### Weather Data:
✅ **All datasets:** Outdoor temperature and humidity  
✅ **BDG2, Singapore:** Solar radiation, wind speed  
✅ **All datasets:** Weather station data aligned with building data  

### Metadata:
✅ **All datasets:** Building type and location  
✅ **BDG2:** Extensive metadata (area, use, industry)  
✅ **I-BLEND:** Occupancy patterns  

---

## Data Format Examples

### BDG2 Format:
```
timestamp,building_id,meter_reading
2016-01-01 00:00:00,0,125.5
2016-01-01 01:00:00,0,118.2
...
```

### Expected Format for Others:
Most datasets follow similar time-series structure:
- Timestamp (datetime)
- Building/meter identifier
- Energy reading (kWh or kW)
- Temperature (°C)
- Humidity (%)
- Additional variables as columns

---

## Filtering BDG2 for Tropical Sites

```python
import pandas as pd

# Load metadata
metadata = pd.read_csv('data/metadata/metadata.csv')

# Filter by timezone (proxy for climate)
# Tropical/subtropical timezones
tropical_zones = ['America/Phoenix', 'America/Los_Angeles', 
                  'US/Central', 'US/Eastern']  # Adjust based on actual data

tropical_buildings = metadata[metadata['timezone'].isin(tropical_zones)]

# Or filter by primary use and location
# Check the metadata columns for climate zone or location info
print(metadata.columns)
print(metadata['site_id'].unique())  # See available sites

# You may need to manually map site_id to climate zones
# based on the paper's supplementary information
```

---

## Recommended Workflow

### Week 1: Setup and Exploration
- [ ] Download BDG2 (immediate access)
- [ ] Explore data structure with provided Jupyter notebooks
- [ ] Identify tropical/subtropical sites in BDG2
- [ ] Set up data processing pipeline

### Week 2: Tropical-Specific Data
- [ ] Request Singapore sub-hourly dataset
- [ ] Request I-BLEND dataset
- [ ] Download Ecuador dataset supplementary materials
- [ ] Document data schemas for each source

### Week 3: Data Integration
- [ ] Harmonize timestamps across datasets
- [ ] Standardize variable names and units
- [ ] Create unified feature engineering pipeline
- [ ] Handle missing data

### Week 4: ML Pipeline Development
- [ ] Split data: training (BDG2) + validation (tropical-specific)
- [ ] Feature selection based on multivariate analysis
- [ ] Baseline model development
- [ ] Evaluate reality gap with real IoT data

---

## Troubleshooting

### If GitHub clone is slow:
```bash
# Try shallow clone
git clone --depth 1 https://github.com/buds-lab/building-data-genome-project-2.git
```

### If Nature Scientific Data papers are paywalled:
- They should be open access, but if you have issues:
- Try accessing through institutional library
- Or use DOI to find preprint versions on ResearchGate or arXiv

### If dataset links are broken:
1. Search for the paper title on Google Scholar
2. Look for "Data Availability" section in the paper
3. Contact corresponding author (email usually in paper)
4. Check if data is on Zenodo, Figshare, or institutional repository

### If you need help with data format:
- BDG2 has extensive Jupyter notebooks in `notebooks/` folder
- Check the paper's supplementary materials
- Look for README files in data repositories

---

## Key Papers to Read

1. **BDG2 Paper:** Miller et al., "The Building Data Genome Project 2", Scientific Data (2020)
   - https://doi.org/10.1038/s41597-020-00712-x

2. **ASHRAE GEPIII Competition:** Miller et al., Science and Technology for the Built Environment (2020)
   - https://doi.org/10.1080/23744731.2020.1795514
   - Preprint: https://arxiv.org/abs/2007.06933

3. **Singapore Dataset:** Search "Sub-hourly measurement datasets 6 real buildings Singapore" (2023)

4. **I-BLEND:** Search "I-BLEND India building energy dataset" (2022)

---

## Contact for Help

### BDG2 Support:
- **GitHub Issues:** https://github.com/buds-lab/building-data-genome-project-2/issues
- **Lead Author:** Clayton Miller, NUS Singapore
- **Lab Website:** https://www.budslab.org/

### Nature Scientific Data Papers:
- Check "Corresponding Author" section in each paper
- Usually includes email for data access questions

### General Building Energy ML Community:
- **Kaggle ASHRAE Competition Forum:** https://www.kaggle.com/c/ashrae-energy-prediction/discussion
- **BuildSys Conference:** Annual conference on building systems and ML

---

## Expected Data Volumes

| Dataset | Approx Size | Download Time | Processing Requirements |
|---------|-------------|---------------|------------------------|
| BDG2 | ~500 MB | 5-10 min | Standard laptop OK |
| Singapore | ~100-500 MB | 2-5 min | Standard laptop OK |
| I-BLEND | ~200-800 MB | 5-10 min | Standard laptop OK |
| Ecuador | ~50-200 MB | 1-3 min | Standard laptop OK |

**Total Storage Needed:** ~2-3 GB for all datasets

**Processing:** All datasets can be processed on a standard laptop with 8GB+ RAM

---

## Success Checklist

After following this guide, you should have:

- [ ] BDG2 dataset downloaded and explored
- [ ] Understanding of BDG2 data structure
- [ ] Access to at least one tropical-specific dataset (Singapore or I-BLEND)
- [ ] List of variables available across datasets
- [ ] Basic data loading and exploration scripts
- [ ] Plan for data integration and ML pipeline

---

## Next Steps After Data Acquisition

1. **Data Quality Assessment:**
   - Check for missing values
   - Identify outliers
   - Validate timestamp continuity

2. **Feature Engineering:**
   - Time-based features (hour, day, season)
   - Weather lag features
   - Building characteristics encoding
   - HVAC operation patterns

3. **Baseline Models:**
   - Simple persistence model
   - Linear regression with weather features
   - Time-series models (ARIMA, Prophet)

4. **Advanced ML:**
   - Gradient boosting (XGBoost, LightGBM)
   - Neural networks (LSTM, Transformers)
   - Ensemble methods

5. **Reality Gap Validation:**
   - Compare predictions on simulated vs. real data
   - Quantify performance difference
   - Identify sources of discrepancy

---

**Good luck with your research! 🚀**

For questions or issues, refer to the comprehensive report: `tropical_building_datasets_comprehensive_report.md`
