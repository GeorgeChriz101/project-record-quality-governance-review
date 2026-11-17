import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font
from docx import Document

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
OUTPUT = Path("output")
DOCS = Path("docs")

for folder in [RAW, PROCESSED, OUTPUT, DOCS]:
    folder.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 1. CREATE 40 SYNTHETIC PROJECT RECORDS
# --------------------------------------------------

rows = []

for i in range(1, 41):
    rows.append({
        "project_id": f"PRJ-{i:03d}",
        "project_name": f"Network Deployment Project {i}",
        "project_owner": f"Owner {((i - 1) % 8) + 1}",
        "approval_status": "Approved",
        "last_update_date": f"2027-05-{((i - 1) % 20) + 1:02d}",
        "document_reference": f"docs/project_{i:03d}.pdf",
        "project_status": ["Planning", "Active", "Active", "Complete"][i % 4]
    })

df = pd.DataFrame(rows)

# --------------------------------------------------
# 2. SEED 10 INTENTIONAL ISSUES
# --------------------------------------------------

# Missing approvals - 2 issues
df.loc[2, "approval_status"] = ""
df.loc[15, "approval_status"] = ""

# Outdated updates - 2 issues
df.loc[5, "last_update_date"] = "2026-10-01"
df.loc[22, "last_update_date"] = "2026-11-15"

# Duplicate IDs - 2 issues
df.loc[10, "project_id"] = "PRJ-010"
df.loc[30, "project_id"] = "PRJ-030"

# Broken / missing document references - 2 issues
df.loc[8, "document_reference"] = ""
df.loc[27, "document_reference"] = "docs/missing_project_file.pdf"

# Missing owners - 2 issues
df.loc[12, "project_owner"] = ""
df.loc[35, "project_owner"] = ""

df.to_csv(
    RAW / "project_records_raw.csv",
    index=False
)

# --------------------------------------------------
# 3. VALIDATION RULES
# --------------------------------------------------

reference_date = pd.Timestamp("2027-05-25")

df["missing_approval"] = (
    df["approval_status"].isna()
    | (df["approval_status"].astype(str).str.strip() == "")
)

df["missing_owner"] = (
    df["project_owner"].isna()
    | (df["project_owner"].astype(str).str.strip() == "")
)

df["last_update_parsed"] = pd.to_datetime(
    df["last_update_date"],
    errors="coerce"
)

df["outdated_update"] = (
    (reference_date - df["last_update_parsed"]).dt.days > 90
)

df["duplicate_project_id"] = (
    df["project_id"].duplicated(keep=False)
)

df["broken_document_reference"] = (
    df["document_reference"].isna()
    | (df["document_reference"].astype(str).str.strip() == "")
    | df["document_reference"].astype(str).str.contains(
        "missing_project_file",
        na=False
    )
)

df["invalid_project_id_format"] = (
    ~df["project_id"].astype(str).str.match(
        r"^PRJ-\d{3}$",
        na=False
    )
)

# Five major validation categories:
# 1 Missing approvals
# 2 Outdated updates
# 3 Duplicate IDs
# 4 Broken document references
# 5 Missing ownership / identifier governance

df["issue_count"] = (
    df[
        [
            "missing_approval",
            "outdated_update",
            "duplicate_project_id",
            "broken_document_reference",
            "missing_owner",
            "invalid_project_id_format"
        ]
    ]
    .astype(int)
    .sum(axis=1)
)

df["quality_status"] = df["issue_count"].apply(
    lambda x: "Review Required" if x > 0 else "Pass"
)

df.to_csv(
    PROCESSED / "project_records_validated.csv",
    index=False
)

# --------------------------------------------------
# 4. EXCEPTION LOG
# --------------------------------------------------

exceptions = df[
    df["issue_count"] > 0
].copy()

def describe_issues(row):
    issues = []

    if row["missing_approval"]:
        issues.append("Missing approval")

    if row["outdated_update"]:
        issues.append("Outdated update")

    if row["duplicate_project_id"]:
        issues.append("Duplicate project ID")

    if row["broken_document_reference"]:
        issues.append("Broken document reference")

    if row["missing_owner"]:
        issues.append("Missing project owner")

    if row["invalid_project_id_format"]:
        issues.append("Invalid project ID format")

    return "; ".join(issues)

exceptions["exception_detail"] = exceptions.apply(
    describe_issues,
    axis=1
)

exceptions.to_csv(
    OUTPUT / "exception_log.csv",
    index=False
)

# --------------------------------------------------
# 5. VALIDATION SUMMARY
# --------------------------------------------------

summary = pd.DataFrame({
    "Validation Rule": [
        "Missing Approval",
        "Outdated Update",
        "Duplicate Project ID",
        "Broken Document Reference",
        "Missing Project Owner",
        "Invalid Project ID Format",
        "Records Requiring Review"
    ],
    "Count": [
        int(df["missing_approval"].sum()),
        int(df["outdated_update"].sum()),
        int(df["duplicate_project_id"].sum()),
        int(df["broken_document_reference"].sum()),
        int(df["missing_owner"].sum()),
        int(df["invalid_project_id_format"].sum()),
        int((df["issue_count"] > 0).sum())
    ]
})

summary.to_csv(
    OUTPUT / "validation_summary.csv",
    index=False
)

# --------------------------------------------------
# 6. EXCEL QUALITY REVIEW WORKBOOK
# --------------------------------------------------

excel_file = OUTPUT / "project_record_quality_review.xlsx"

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Validated Records",
        index=False
    )

    exceptions.to_excel(
        writer,
        sheet_name="Exception Log",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Validation Summary",
        index=False
    )

wb = load_workbook(excel_file)

for ws in wb.worksheets:
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for column in ws.columns:
        max_length = 0
        letter = column[0].column_letter

        for cell in column:
            try:
                max_length = max(
                    max_length,
                    len(str(cell.value or ""))
                )
            except Exception:
                pass

        ws.column_dimensions[letter].width = min(
            max_length + 2,
            45
        )

wb.save(excel_file)

# --------------------------------------------------
# 7. WORD QUALITY REVIEW REPORT
# --------------------------------------------------

doc = Document()

doc.add_heading(
    "Project Record Quality and Governance Review",
    0
)

doc.add_paragraph(
    "This report summarizes the results of a synthetic project "
    "record quality review covering 40 sample project records."
)

doc.add_heading("Review Scope", level=1)

for item in [
    "Missing approvals",
    "Outdated project updates",
    "Duplicate project IDs",
    "Broken document references",
    "Missing ownership",
    "Identifier format consistency"
]:
    doc.add_paragraph(item, style="List Bullet")

doc.add_heading("Results", level=1)

doc.add_paragraph(
    f"Records reviewed: {len(df)}"
)

doc.add_paragraph(
    f"Records requiring review: {(df['issue_count'] > 0).sum()}"
)

doc.add_paragraph(
    f"Total validation exceptions: {df['issue_count'].sum()}"
)

doc.add_heading("Governance Purpose", level=1)

doc.add_paragraph(
    "The review demonstrates how repeatable validation rules can "
    "help improve project record completeness, consistency, ownership, "
    "documentation quality, and reporting reliability."
)

doc.save(
    OUTPUT / "project_record_quality_review.docx"
)

print("")
print("===================================")
print("PROJECT BUILD COMPLETE")
print("===================================")
print("Records reviewed:", len(df))
print(
    "Records requiring review:",
    int((df["issue_count"] > 0).sum())
)
print("Excel report:", excel_file)
print("Exception log: output/exception_log.csv")
