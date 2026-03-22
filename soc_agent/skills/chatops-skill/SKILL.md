---
name: chatops-skill
description: Enables the agent to communicate with human security analysts for notifications and high-stakes confirmations (Human-in-the-loop).
---

### ChatOps and Human Interaction Implementation
You are equipped with the capability to send rich notifications and action requests to human security analysts via ChatOps (Google Chat / Webhooks). Use this skill when you need a human to perform a task, confirm a state-changing action, or stay informed about a critical event.

**Instructions:**
1. **Critical Actions (HITL):** Before performing any irreversible or high-risk state-changing actions (e.g., isolating a host, blocking a user account, or wiping a machine), you MUST propose the action to a human analyst for confirmation using the `request_human_confirmation` tool.
2. **Incident Notifications:** When you identify a confirmed CRITICAL or HIGH severity incident, immediately notify the human team using the `notify_human_incident` tool.
3. **Custom Alerts:** Use the `send_chatops_card` tool for general-purpose notifications or status reports that require a structured card format.
4. **Transparency:** When you send a notification or a request to a human, include this in your orchestrator synthesis (e.g., "I've requested a human confirmation for the host isolation action...").
5. **Human Context:** Always provide clear rationale and evidence when requesting human input, so the analyst has the necessary context to make a decision.

**Tools Summary:**
- **request_human_confirmation:** Propose a specific action with context for approval/denial.
- **notify_human_incident:** Alert the team to a confirmed incident with severity and IDs.
- **send_chatops_card:** Send any custom card with title, subtitle, and sections.

### Example Card Layout Patterns
When using `send_chatops_card`, you can use these patterns for the `sections` argument:

**1. IOC Enrichment Layout (decoratedText)**
```json
[
  { "widgets": [
    { "decoratedText": { "topLabel": "Vendor A", "text": "Tagged: Fancy Bear / APT28", "startIcon": { "knownIcon": "DESCRIPTION" } } },
    { "decoratedText": { "topLabel": "Vendor B", "text": "45/70 Malicious detections", "startIcon": { "knownIcon": "BUG_REPORT" } } },
    { "buttonList": { "buttons": [{ "text": "View Full Report", "onClick": { "openLink": { "url": "https://..." } } }] } }
  ]}
]
```

**2. Runtime / Threat Detection Layout (textParagraph + buttons)**
```json
[
  { "widgets": [
    { "textParagraph": { "text": "Pod <b>auth-api-88x</b> is consuming 100% CPU on Cryptominer signatures. Should I kill and redeploy?" } },
    { "buttonList": { "buttons": [
      { "text": "Kill & Redeploy", "onClick": { "openLink": { "url": "https://..." } } },
      { "text": "Debug Console", "onClick": { "openLink": { "url": "https://..." } } }
    ]} }
  ]}
]
```

**3. User/Entity Context (impossible travel)**
```json
[
  { "widgets": [
    { "decoratedText": { "topLabel": "Current Login", "text": "London, UK (IP: 85.112.x.x)", "startIcon": { "knownIcon": "FLIGHT_TAKEOFF" } } },
    { "decoratedText": { "topLabel": "Previous Login", "text": "New York, US (IP: 12.34.x.x)", "startIcon": { "knownIcon": "FLIGHT_LAND" } } },
    { "buttonList": { "buttons": [ { "text": "Confirm Identity", "onClick": { "openLink": { "url": "https://..." } } } ] } }
  ]}
]
```

### Reference Scenarios for ChatOps
The following scenarios are pre-defined as high-value for human interaction. Use the tools indicated for each:

**Access & Identity (Use `request_human_confirmation`)**
- `ai_credential_reset_approval`: Request approval before forcing a password reset on a high-value account.
- `ai_privileged_session_recording`: Notify and request logic for initiating recording on a sensitive session.
- `ai_stale_account_cleanup`: Propose deletion of identified stale or dormant accounts.
- `ai_suspicious_login_location`: Request user/analyst confirmation for logins from new geo-locations.
- `ai_user_privilege_audit`: Request privilege review for users with excessive permissions.
- `temp_admin_request`: Propose and approve temporary administrative/break-glass access.
- `mfa_api_key_alert`: Notify and request MFA enforcement for vulnerable service keys.
- `ai_security_group_audit`: Propose modifications to firewall groups or IAM policies after a security audit.

**Containment & Remediation (Use `request_human_confirmation`)**
- `ai_brute_force_source_block`: Request approval to block an IP address at the firewall after brute force detection.
- `ai_malicious_container_kill`: Request approval to terminate a compromised K8s pod or container.
- `ai_suspicious_process_kill`: Request approval before killing a process on a critical server.
- `ai_wipe_host_approval`: **MANDATORY HITL**: Never wipe a host without explicit human approval.
- `ai_data_exfiltration_block`: Request to block an egress point once exfiltration is suspected.
- `ai_malicious_domain_sinkhole`: Propose redirection of malicious domain traffic to a sinkhole.
- `host_isolation_approval`: Propose isolating an infected host from the network.
- `vulnerability_patch_approval`: Seek approval for applying emergency security patches to production systems.

**Alerting & Intel (Use `notify_human_incident` / `send_chatops_card`)**
- `ai_threat_intel_sharing`: Use `send_chatops_card` to share new IOCs discovered during an investigation.
- `ai_compliance_violation_alert`: Notify humans of identified policy or compliance drifts.
- `ai_dns_exfiltration_detection`: Notify humans of anomalous DNS patterns indicative of tunneling.
- `ai_forensic_image_approval`: Request permission to take a forensic disk/memory image.
- `ai_threat_hunt_hypothesis`: Present a new threat hunting hypothesis to human analysts for feedback.
- `ioc_enrichment_card`: Visual card showing multi-vendor intelligence for an IP, Domain, or Hash.
- `malware_sandbox_report`: Summary of automated sandbox analysis (static and dynamic behavior).
- `phishing_report_summary`: Overview of user-reported phishing attempts and identified risk.
- `ai_canary_token_deployment`: Propose the deployment of honeytokens/canaries in sensitive environments.
- `shadow_it_discovery`: Alert on newly discovered unmanaged cloud resources or applications.

**Operational Workflow (Use `send_chatops_card` / `request_human_confirmation`)**
- `ai_draft_comms_review`: Propose a draft email/notification for a human to review before sending.
- `ai_playbook_selection`: Ask the human which strategy to prioritize if multiple playbooks apply.
- `ai_incident_summary_confirm`: Request a human to review your final incident summary before closure.
- `ai_incident_closure_confirm`: Final sign-off required from an analyst before officially closing an incident.
- `ai_incident_retrospective_request`: Trigger a post-mortem or retrospective task after a significant incident.
- `bulk_deletion_verification`: Require human dual-control for any bulk deletion of logs or records.
- `ai_false_positive_tuning`: Propose logic changes to detection rules to reduce noise.
- `ai_user_interview_request`: Ask an analyst to interview a user to confirm suspicious (but potentially benign) activity.
- `ai_data_classification_request`: Request a human to classify sensitive data found in an unconventional location.
- `ai_vulnerability_revalidation`: Request a human to manually verify that a reported vulnerability has been fixed.
