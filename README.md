# Project Record Quality and Governance Review

A PMO governance portfolio project demonstrating how project records can be validated for completeness, consistency, ownership, approval status, documentation quality, and naming standards.

## Project Overview

This project reviews 40 synthetic project records using repeatable validation rules.

Intentional quality issues are included so the workflow can identify exceptions and generate a structured governance review.

## Tools Used

- Python
- pandas
- CSV
- Excel
- openpyxl
- Microsoft Word
- Git

## Key Features

- 40 synthetic project records
- Repeatable validation rules
- Missing approval detection
- Outdated record detection
- Duplicate project ID detection
- Broken document reference detection
- Missing owner detection
- Project ID format validation
- Exception logging
- Validation summary
- Excel quality-review workbook
- Word review report
- Governance documentation
- Meeting templates
- Quality-review checklist

## Project Structure

project-record-quality-governance-review/

data/raw/
- project_records_raw.csv

data/processed/
- project_records_validated.csv

output/
- exception_log.csv
- validation_summary.csv
- project_record_quality_review.xlsx
- project_record_quality_review.docx

docs/
- data_dictionary.md
- validation_rules.md
- project_methodology.md
- folder_and_naming_conventions.md
- quality_review_checklist.md
- meeting_agenda.md
- meeting_minutes_template.md
- exception_management_process.md
- project_summary.md

scripts/
- build_project.py

README.md
requirements.txt
.gitignore

## Governance Workflow

Project Register

↓

Validation Rules

↓

Quality Checks

↓

Exception Identification

↓

Exception Log

↓

Corrective Action

↓

Revalidation

↓

Governance Reporting

## Validation Areas

### Approvals

Checks whether required approval information exists.

### Record Currency

Identifies project records that have not been updated within the required review period.

### Unique IDs

Detects duplicate project identifiers.

### Documentation

Checks whether project documentation references are present and valid.

### Ownership and Naming Standards

Checks assigned ownership and project ID naming conventions.

## Exception Log

Records that fail validation are placed into an exception log for review and corrective action.

## Excel Workbook

The Excel workbook includes:

- Validated Records
- Exception Log
- Validation Summary

## Documentation

Supporting documentation includes:

- Data dictionary
- Validation rules
- Project methodology
- Folder and naming conventions
- Quality-review checklist
- Meeting agenda
- Meeting minutes template
- Exception management process

## Run the Project

Activate the virtual environment:

    source .venv/bin/activate

Run:

    python scripts/build_project.py

## Purpose

This project demonstrates practical PMO governance skills, including record validation, data-quality review, documentation standards, exception management, reporting, and process control.

All project data is synthetic and created for portfolio demonstration purposes.
