# MRI Parameter Analyzer

A Python tool for analyzing DICOM files, extracting MRI parameters, storing them in a PostgreSQL database, and providing a web dashboard for visualization and abnormality detection.

## Features

- DICOM file parsing and parameter extraction
- PostgreSQL database storage with optimized schema
- Interactive web dashboard for data visualization
- Statistical analysis and abnormality detection
- Configurable parameter thresholds
- Test data generation utilities

## Project Structure

```
MRI-Param-abnormalities/
├── src/
│   └── mri_param_analyzer/
│       ├── core/                 # Core business logic
│       │   ├── database.py       # Database operations
│       │   └── dicom_reader.py   # DICOM file processing
│       ├── dashboard/            # Web dashboard
│       │   └── app.py           # Dash application
│       ├── utils/               # Utility functions
│       │   └── data_formatter.py # Data formatting utilities
│       └── models/              # Data models (future)
├── tests/
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── scripts/
│   └── generate_test_dicom.py  # Test data generation
├── data/
│   ├── raw/                    # Raw DICOM files
│   ├── processed/              # Processed data
│   └── test/                   # Test data
├── docs/                       # Documentation
├── config/                     # Configuration files
│   └── database.conf.template  # Database config template
├── requirements.txt            # Python dependencies
├── setup.py                   # Package setup
└── README.md                  # This file
```

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd MRI-Param-abnormalities
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

## Configuration

1. Copy the database configuration template:
```bash
cp config/database.conf.template config/database.conf
```

2. Edit `config/database.conf` with your PostgreSQL credentials:
```ini
[database]
host = localhost
port = 5432
dbname = DICOM_Database
user = your_username
password = your_password

[paths]
dicom_data_dir = /path/to/your/dicom/data
output_dir = /path/to/output
```

## Database Setup

1. Ensure PostgreSQL is running
2. Create the database and tables:
```bash
python src/mri_param_analyzer/core/database.py
```

## Usage

### Processing DICOM Files
```bash
python src/mri_param_analyzer/core/dicom_reader.py
```

### Running the Dashboard
```bash
python src/mri_param_analyzer/dashboard/app.py
```

The dashboard will be available at `http://localhost:8050`

### Generating Test Data
```bash
python scripts/generate_test_dicom.py
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black src/ tests/ scripts/
```

### Type Checking
```bash
mypy src/
```

## Database Schema

The application uses two main tables:

- `patient_series`: Stores basic patient and series information
- `protocol_parameters`: Stores detailed MRI parameters with foreign key relationship

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 