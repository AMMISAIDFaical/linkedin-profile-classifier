# Security and Compliance

This project processes public profile information. Treat all data and credentials with care and ensure your usage complies with applicable terms and laws.

## Secrets management

- Local development: Store credentials in a local `.env` file (gitignored). Do not share or commit it.
- CI/CD: Use repository/environment secrets in GitHub Actions or your CI system.
- Rotation: If secrets were ever committed, rotate them immediately. Assume they are compromised.

## Data protection

- Limit data collection to what you need and what you are authorized to process.
- Retain outputs only as long as necessary and restrict access to authorized users.
- If outputs contain sensitive fields, encrypt at rest and in transit.

## External services

- Bright Data: Review and comply with Bright Data's terms of service and usage policies.
- LLM providers: Ensure your token and model choice comply with your organization's policies.

## Auditing and governance

- Keep records of when classifications were executed and by whom.
- Consider adding a simple audit log that includes input hashes and output labels per row.

## Recommended next steps

- Add a secrets scanning tool (e.g., GitHub secret scanning) and pre-commit hooks.
- Parameterize file paths and remove absolute paths from code to reduce accidental data leakage.
- Add structured logging and correlation IDs for traceability.
