# 📁 File Guide - What to Read and Use

## 🎯 Main Deliverable Files (Start Here!)

### 1. **README.md** (12 KB) ⭐ START HERE
**Purpose:** Package overview and navigation guide  
**Read Time:** 5 minutes  
**What's Inside:**
- Quick overview of all 7 datasets
- Top 3 recommendations with immediate access links
- Quick start instructions (3 steps)
- Requirements checklist

**When to Use:** First file to read for overall understanding

---

### 2. **EXECUTIVE_SUMMARY.md** (12 KB) ⭐ KEY FINDINGS
**Purpose:** High-level findings and recommendations  
**Read Time:** 5 minutes  
**What's Inside:**
- Search results overview (7 datasets, 4 tropical-specific)
- Detailed description of top 3 datasets
- Data characteristics summary
- Access strategy and action plan
- Success criteria checklist

**When to Use:** For quick decision-making and understanding key findings

---

### 3. **QUICK_START_GUIDE.md** (12 KB) ⭐ IMMEDIATE ACTION
**Purpose:** Step-by-step access instructions  
**Read Time:** 10 minutes  
**What's Inside:**
- Detailed access instructions for each dataset
- Code examples for downloading and loading data
- Filtering instructions for tropical sites
- Troubleshooting guide
- Week-by-week workflow plan

**When to Use:** When you're ready to start downloading and using the datasets

---

### 4. **tropical_building_datasets_comprehensive_report.md** (20 KB) ⭐ COMPLETE REFERENCE
**Purpose:** Complete detailed report with all information  
**Read Time:** 30 minutes  
**What's Inside:**
- Detailed description of all 7 datasets
- Complete variable lists and data formats
- Access methods and repository information
- Citation information for all datasets
- ML readiness assessment
- Reality gap considerations
- Dataset selection guide by use case
- Complete contact information

**When to Use:** For comprehensive research, citation information, and detailed technical specifications

---

## 📊 Data Files (For Analysis)

### 5. **datasets_comparison_table.csv** (2.3 KB)
**Purpose:** Side-by-side comparison of all datasets  
**Format:** CSV spreadsheet  
**Columns:**
- Dataset Name
- Climate Coverage
- Tropical (Yes/Partial)
- Frequency
- Buildings
- Duration
- ML Ready
- Access Type
- Main URL
- DOI
- Key Variables

**When to Use:** For quick comparison, sorting, and filtering datasets by criteria

---

### 6. **tropical_datasets_quick_access.csv** (658 bytes)
**Purpose:** Quick reference for tropical-specific datasets only  
**Format:** CSV spreadsheet  
**Columns:**
- Dataset Name
- Location (Climate)
- Access URL
- Priority Rating

**When to Use:** When you only want tropical/hot-humid climate datasets

---

### 7. **tropical_building_datasets_catalog.json** (6.4 KB)
**Purpose:** Machine-readable catalog of all datasets  
**Format:** JSON  
**Structure:** Array of dataset objects with all metadata  
**Fields per Dataset:**
- name, source, climate_coverage
- tropical_sites, data_frequency
- time_range, buildings, meters
- variables, format, access
- url, doi, publication
- ml_ready, reality_gap, notes

**When to Use:** For programmatic access, automation, or integration with other tools

---

### 8. **dataset_search_summary.json** (2.5 KB)
**Purpose:** Summary of search results and recommendations  
**Format:** JSON  
**Contents:**
- Total counts (datasets, tropical-specific, accessible)
- Top 3 recommendations with details
- Key repositories searched
- Data characteristics summary
- Tropical climate coverage by region

**When to Use:** For quick programmatic access to summary statistics

---

## 🔍 Supporting Files (Background Research)

### Scraped Web Content:
- **bdg2_github_details.md** (16 KB) - BDG2 GitHub repository details
- **dataset2_building_genome.md** (69 KB) - BDG2 publication details
- **dataset3_hot_humid_commercial.md** (103 KB) - Ecuador dataset paper
- **dataset1_tropical_energy.md** (52 KB) - Tropical courtyard dataset paper

### Search Results (CSV):
All web search results saved for reference:
- ashrae_tropical_datasets.csv
- tropical_ieq_datasets.csv
- repository_tropical_data.csv
- scientific_data_building.csv
- singapore_building_data.csv
- india_building_data.csv
- brazil_building_data.csv
- zenodo_datasets.csv
- And more...

**When to Use:** For deep-dive research, finding additional sources, or verification

---

## 📖 Recommended Reading Order

### For Quick Start (30 minutes total):
1. **README.md** (5 min) - Overview
2. **EXECUTIVE_SUMMARY.md** (5 min) - Key findings
3. **QUICK_START_GUIDE.md** (10 min) - How to access
4. **datasets_comparison_table.csv** (10 min) - Compare options

### For Comprehensive Understanding (1 hour):
1. **README.md** (5 min)
2. **EXECUTIVE_SUMMARY.md** (5 min)
3. **tropical_building_datasets_comprehensive_report.md** (30 min)
4. **QUICK_START_GUIDE.md** (10 min)
5. Review CSV files (10 min)

### For Immediate Action (15 minutes):
1. **QUICK_START_GUIDE.md** - Read "Quick Start (3 Steps)" section
2. Execute: `git clone https://github.com/buds-lab/building-data-genome-project-2.git`
3. Explore BDG2 data structure

---

## 🎯 Use Case Guide

### "I need to start immediately"
→ Read: **QUICK_START_GUIDE.md** (sections: Quick Start, Immediate Access)  
→ Action: Clone BDG2 repository

### "I need tropical-specific data only"
→ Read: **EXECUTIVE_SUMMARY.md** (section: Top 3 Recommendations)  
→ Use: **tropical_datasets_quick_access.csv**  
→ Focus on: Singapore, I-BLEND, Ecuador datasets

### "I need complete technical details"
→ Read: **tropical_building_datasets_comprehensive_report.md**  
→ Use: **datasets_comparison_table.csv**

### "I need to cite these datasets"
→ Read: **tropical_building_datasets_comprehensive_report.md** (section: Citation Information)  
→ Or: **EXECUTIVE_SUMMARY.md** (section: Key Citations)

### "I need programmatic access"
→ Use: **tropical_building_datasets_catalog.json**  
→ Use: **dataset_search_summary.json**

### "I need to compare datasets"
→ Use: **datasets_comparison_table.csv**  
→ Read: **tropical_building_datasets_comprehensive_report.md** (section: Dataset Selection Guide)

---

## 🗂️ File Organization

```
/home/sandbox/
│
├── 📄 Main Documentation (READ THESE)
│   ├── README.md ⭐ START HERE
│   ├── EXECUTIVE_SUMMARY.md ⭐ KEY FINDINGS
│   ├── QUICK_START_GUIDE.md ⭐ IMMEDIATE ACTION
│   ├── tropical_building_datasets_comprehensive_report.md ⭐ COMPLETE REFERENCE
│   └── FILE_GUIDE.md (this file)
│
├── 📊 Data Files (USE THESE)
│   ├── datasets_comparison_table.csv
│   ├── tropical_datasets_quick_access.csv
│   ├── tropical_building_datasets_catalog.json
│   └── dataset_search_summary.json
│
└── 🔍 Supporting Files (REFERENCE)
    ├── Scraped content (*.md files)
    └── Search results (*.csv files)
```

---

## 💡 Quick Tips

### For Researchers:
- Start with **EXECUTIVE_SUMMARY.md** for overview
- Read **tropical_building_datasets_comprehensive_report.md** for citations
- Use **datasets_comparison_table.csv** for comparison

### For Developers:
- Use **tropical_building_datasets_catalog.json** for programmatic access
- Read **QUICK_START_GUIDE.md** for code examples
- Start with BDG2 for immediate testing

### For Students:
- Start with **README.md** for orientation
- Follow **QUICK_START_GUIDE.md** step-by-step
- Use **EXECUTIVE_SUMMARY.md** for assignment summaries

### For Decision Makers:
- Read **EXECUTIVE_SUMMARY.md** only (5 minutes)
- Review **tropical_datasets_quick_access.csv**
- Check "Requirements Met" section

---

## 📞 Need Help?

### Can't find what you need?
- Check the **TABLE OF CONTENTS** in each markdown file
- Use Ctrl+F (Find) to search within documents
- Start with **README.md** for navigation

### Technical questions about datasets?
- See **tropical_building_datasets_comprehensive_report.md** (section: Contact Information)
- Check dataset GitHub repositories for issues/discussions
- Contact dataset authors (emails in publications)

### Access problems?
- See **QUICK_START_GUIDE.md** (section: Troubleshooting)
- Check **tropical_building_datasets_comprehensive_report.md** (section: How to Access)

---

## ✅ Checklist: Have You Read?

Before starting your research, make sure you've reviewed:

- [ ] **README.md** - Overall understanding
- [ ] **EXECUTIVE_SUMMARY.md** - Key findings
- [ ] **QUICK_START_GUIDE.md** - Access instructions
- [ ] **datasets_comparison_table.csv** - Dataset comparison
- [ ] Selected relevant sections from **comprehensive_report.md**

Once complete, you're ready to:
- [ ] Download BDG2 dataset
- [ ] Request tropical-specific datasets
- [ ] Start your ML pipeline development

---

## 🎉 Summary

**8 main deliverable files** created for you:

1. **README.md** - Start here
2. **EXECUTIVE_SUMMARY.md** - Key findings (5 min)
3. **QUICK_START_GUIDE.md** - How to access (10 min)
4. **tropical_building_datasets_comprehensive_report.md** - Complete reference (30 min)
5. **datasets_comparison_table.csv** - Comparison spreadsheet
6. **tropical_datasets_quick_access.csv** - Tropical-only quick reference
7. **tropical_building_datasets_catalog.json** - Machine-readable catalog
8. **dataset_search_summary.json** - Summary statistics

**Plus:** 40+ supporting files with scraped content and search results

**Total Package:** Complete research compilation on tropical building energy datasets

---

**Next Step:** Open **README.md** to begin! 🚀

---

*File Guide Version 1.0 - January 2026*
