# Email Analyzer

Parses email data and generates frequency analysis reports.

## Features
- Parses mbox format email files
- Counts email and domain frequency by sender
- Generates summary reports

## Version History
- **v1** (archive/v1_basic.py): Basic email parsing
- **v2** (archive/v2_enhanced.py): Added frequency counting and basic report generation
- **v3** (email_summary.py): Added report generation ⭐ Current

## Usage
```bash
# Run analyzer
python email_summary.py
```

## File Structure
```
email_analyzer/
├── email_summary.py    # Main script (v3)
├── data/               # Input files
├── outputs/            # Generated reports
└── archive/            # Previous versions
```

## Input
- `data/mbox-short.txt` - Sample email data

## Output
- `outputs/summary_report.txt` - Email frequency report