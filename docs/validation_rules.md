# Validation Rules

The project applies repeatable governance checks to project records.

## Rule 1 - Required Approval

Every project record should include an approval status.

Records without approval information are flagged.

## Rule 2 - Current Update Date

Project records should be updated regularly.

For this project, a record is considered outdated when the latest update is more than 90 days before the review date.

## Rule 3 - Unique Project ID

Every project should have a unique identifier.

Duplicate IDs are flagged for review.

## Rule 4 - Supporting Document Reference

Each project should contain a reference to the relevant supporting documentation.

Blank or intentionally broken references are flagged.

## Rule 5 - Ownership and Naming Governance

Project records should have:

- An assigned owner
- A project ID following the required naming convention

Expected ID format:

PRJ-###

These checks demonstrate how basic governance controls can improve record quality.
