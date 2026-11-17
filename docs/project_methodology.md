# Project Methodology

## Step 1 - Create the Project Register

The project begins with 40 synthetic project records.

Each record includes:

- Project ID
- Project name
- Owner
- Approval status
- Last update date
- Document reference
- Project status

## Step 2 - Seed Quality Issues

Intentional data-quality problems are added to simulate real project governance issues.

Examples include:

- Missing approvals
- Outdated records
- Duplicate IDs
- Broken document references
- Missing owners

## Step 3 - Apply Validation Rules

Python and pandas are used to apply repeatable checks across the project register.

## Step 4 - Flag Exceptions

Records failing one or more validation rules are placed into an exception log.

## Step 5 - Summarize Findings

A validation summary reports how many records fail each governance rule.

## Step 6 - Prepare Review Outputs

The project creates:

- Validated project register
- Exception log
- Validation summary
- Excel quality-review workbook
- Word quality-review report

## Step 7 - Support Governance Review

The final documentation provides naming standards, meeting templates, and review checklists so the process can be repeated.
