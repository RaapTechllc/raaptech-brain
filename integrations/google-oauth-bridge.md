---
type: Reference
title: Google OAuth Bridge
description: How to use Google OAuth credentials for knowledge sync, Google Workspace, and cloud operations.
resource: C:/Users/Kyle/.gemini/oauth_creds.json
tags: [integrations, google, oauth, sync]
timestamp: 2026-07-06T16:30:00Z
---

# Google OAuth Bridge

**Credential location:** `C:\Users\Kyle\.gemini\oauth_creds.json`
**Status:** Active — token valid, refresh token present, expiry 2026-07-06+

## Scopes Available

| Scope | Purpose |
|---|---|
| `userinfo.email` | Identity verification |
| `userinfo.profile` | Basic profile data |
| `cloud-platform` | Full Google Cloud access |
| `openid` | OpenID Connect |

## What This Unlocks

With `cloud-platform` scope, agents can:

1. **Google Drive sync** — Pull/push knowledge documents between Drive and the brain
2. **Google Calendar** — Read/write calendar events for scheduling and context
3. **Gmail** — Read/send emails for client communication
4. **Google Cloud** — BigQuery, Cloud Storage, Cloud Run for data pipelines
5. **Google Docs/Sheets** — Read/write collaborative documents

## Usage Pattern

### Python (recommended)

```python
import json
from pathlib import Path
from google.oauth2.credentials import Credentials

creds_path = Path.home() / ".gemini" / "oauth_creds.json"
with open(creds_path) as f:
    creds_data = json.load(f)

credentials = Credentials(
    token=creds_data["access_token"],
    refresh_token=creds_data["refresh_token"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=creds_data.get("client_id"),
    client_secret=creds_data.get("client_secret"),
    scopes=creds_data["scope"].split(" "),
)
```

### Hermes CLI

```bash
# Check auth status
hermes auth status

# Add Google credential to Hermes pool
hermes auth add google --token-file ~/.gemini/oauth_creds.json
```

## Sync Protocol

### Brain → Google Drive (push)

1. Agent reads concept from brain
2. Agent converts to Google Doc format
3. Agent writes to designated Drive folder
4. Agent updates concept's `resource` field with Drive URL

### Google Drive → Brain (pull)

1. Agent lists files in designated Drive folder
2. Agent downloads new/changed files
3. Agent converts to OKF markdown format
4. Agent writes to brain with proper frontmatter
5. Agent logs sync in `log.md`

## Security Rules

- Never print the access token or refresh token
- Token refresh is automatic via Google client libraries
- If token is revoked, re-authenticate via `gcloud auth application-default login`
- Credentials file is gitignored — never commit to any repo