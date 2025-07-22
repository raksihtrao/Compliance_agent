# Sample Compliance Prompts for Testing

## GDPR Compliance Check Prompt

**Compliance Protocol Name:** GDPR Data Protection Audit
**Protocol Description / Rule:** Check document for compliance with General Data Protection Regulation (GDPR) requirements including lawful basis, consent, data minimization, retention, and data subject rights.
**What to Flag:** Unauthorized data collection, missing consent mechanisms, excessive data retention, failure to honor data subject rights, inadequate security measures, unauthorized international transfers, improper handling of children's data.
**Severity Threshold:** High
**Expected Output Format:** JSON
**Citation Required:** Yes
**Language:** English

## HIPAA Compliance Check Prompt

**Compliance Protocol Name:** HIPAA PHI Protection Audit
**Protocol Description / Rule:** Check document for compliance with Health Insurance Portability and Accountability Act (HIPAA) requirements including PHI protection, minimum necessary standard, and proper safeguards.
**What to Flag:** Unauthorized disclosure of PHI, lack of minimum necessary standard, missing safeguards, improper sharing with non-authorized parties, inadequate security measures, failure to obtain patient authorization.
**Severity Threshold:** High
**Expected Output Format:** JSON
**Citation Required:** Yes
**Language:** English

## SOC 2 Compliance Check Prompt

**Compliance Protocol Name:** SOC 2 Security Controls Audit
**Protocol Description / Rule:** Check document for compliance with SOC 2 Trust Services Criteria including security, availability, processing integrity, confidentiality, and privacy.
**What to Flag:** Weak access controls, missing security policies, inadequate monitoring, poor change management, insufficient backup procedures, lack of incident response plans.
**Severity Threshold:** Medium
**Expected Output Format:** JSON
**Citation Required:** Yes
**Language:** English

## PCI-DSS Compliance Check Prompt

**Compliance Protocol Name:** PCI-DSS Cardholder Data Protection
**Protocol Description / Rule:** Check document for compliance with Payment Card Industry Data Security Standard (PCI-DSS) requirements for protecting cardholder data.
**What to Flag:** Unencrypted cardholder data, weak authentication systems, missing security policies, inadequate network segmentation, improper data storage, lack of access controls.
**Severity Threshold:** High
**Expected Output Format:** JSON
**Citation Required:** Yes
**Language:** English

## How to Use These Prompts:

1. Copy one of the prompts above
2. Go to the Compliance Check Agent in your Streamlit app
3. Fill in the form fields with the prompt details
4. Click "Done" to lock in the prompt
5. Upload the corresponding test document:
   - Use `test_gdpr_violation.txt` for GDPR testing
   - Use `test_hipaa_violation.txt` for HIPAA testing
6. Click "Run Compliance Check"
7. Review the detailed results showing violations and compliant points

## Expected Results:

The system should detect multiple violations in each test document and provide:
- Specific violation details with citations
- Compliance summary
- Overall assessment (likely "Non-Compliant")
- Recommendations for remediation 