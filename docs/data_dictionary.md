# Data Dictionary

## project_id

Unique identifier for a project record.

Expected format:

PRJ-001

## project_name

Descriptive project name.

## project_owner

Person responsible for the project record.

## approval_status

Indicates whether the required project approval has been recorded.

## last_update_date

Date the project record was most recently updated.

## document_reference

Reference to the supporting project document.

## project_status

Current project status.

Examples:

- Planning
- Active
- Complete

## missing_approval

Flag showing that required approval information is missing.

## missing_owner

Flag showing that the project has no assigned owner.

## outdated_update

Flag showing that the project record has not been updated within the defined review period.

## duplicate_project_id

Flag showing that the project ID appears more than once.

## broken_document_reference

Flag identifying a missing or invalid supporting document reference.

## invalid_project_id_format

Flag identifying a project ID that does not meet the naming convention.

## issue_count

Total number of validation issues identified for the record.

## quality_status

Overall result of the validation review.

Values include:

- Pass
- Review Required
