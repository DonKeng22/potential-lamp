# Data Scripts

This directory contains scripts for managing and generating data for the Field Hockey Broadcasting Platform.

## 📁 Structure

```
data/scripts/
├── generate_sample_data.py   # Script to generate sample user, stream, and player data
└── README.md                 # This file
```

## 🚀 Usage

### Generating Sample Data

To populate your database with sample data for development and testing, run the `generate_sample_data.py` script:

```bash
python generate_sample_data.py
```

This script will:
- Create sample user accounts.
- Add placeholder live streams.
- Populate player profiles with basic information and statistics.

## 📝 Notes

- Ensure your database is running and accessible before running these scripts.
- These scripts are intended for development and testing environments only. Do not use them in production.
- You may need to configure database connection details in the script or via environment variables.
