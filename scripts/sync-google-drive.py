#!/usr/bin/env python3
"""Google Drive sync bridge for raaptech-brain.

Uses the Google OAuth credentials at ~/.gemini/oauth_creds.json to push/pull
knowledge documents between the brain and Google Drive.

Prerequisites:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Usage:
    python scripts/sync-google-drive.py --pull          # Download from Drive → brain
    python scripts/sync-google-drive.py --push          # Upload brain → Drive
    python scripts/sync-google-drive.py --list          # List files in Drive brain folder
    python scripts/sync-google-drive.py --status        # Check auth status
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

BUNDLE_ROOT = Path(__file__).resolve().parent.parent
CREDS_PATH = Path.home() / ".gemini" / "oauth_creds.json"
DRIVE_FOLDER_NAME = "raaptech-brain"  # Top-level folder in Google Drive


def get_credentials() -> dict:
    """Load OAuth credentials from the Gemini creds file."""
    if not CREDS_PATH.exists():
        print(f"❌ No credentials found at {CREDS_PATH}")
        print("   Run: gcloud auth application-default login")
        sys.exit(1)
    with open(CREDS_PATH) as f:
        return json.load(f)


def build_service(creds_data: dict):
    """Build an authenticated Google Drive service object."""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials(
        token=creds_data["access_token"],
        refresh_token=creds_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_data.get("client_id"),
        client_secret=creds_data.get("client_secret"),
        scopes=creds_data.get("scope", "").split(" "),
    )

    return build("drive", "v3", credentials=credentials)


def find_or_create_folder(service) -> str:
    """Find or create the raaptech-brain folder in Google Drive."""
    # Search for existing folder
    results = service.files().list(
        q=f"name='{DRIVE_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)",
        pageSize=1,
    ).execute()

    files = results.get("files", [])
    if files:
        folder_id = files[0]["id"]
        print(f"📁 Found existing folder: {DRIVE_FOLDER_NAME} ({folder_id})")
        return folder_id

    # Create new folder
    folder_metadata = {
        "name": DRIVE_FOLDER_NAME,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    folder_id = folder["id"]
    print(f"📁 Created folder: {DRIVE_FOLDER_NAME} ({folder_id})")
    return folder_id


def list_drive_files(service, folder_id: str):
    """List all markdown files in the brain folder."""
    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType='text/markdown' and trashed=false",
        fields="files(id, name, modifiedTime, size)",
        pageSize=100,
    ).execute()
    return results.get("files", [])


def pull_from_drive(service, folder_id: str):
    """Download all markdown files from Drive → brain."""
    from googleapiclient.http import MediaIoBaseDownload
    import io

    files = list_drive_files(service, folder_id)
    if not files:
        print("📭 No markdown files found in Drive folder.")
        return

    print(f"📥 Pulling {len(files)} files from Drive...")
    for f in files:
        dest = BUNDLE_ROOT / f["name"]
        request = service.files().get_media(fileId=f["id"])
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        dest.write_bytes(fh.getvalue())
        print(f"   ✅ {f['name']} ({f.get('size', '?')} bytes)")


def push_to_drive(service, folder_id: str):
    """Upload all markdown files from brain → Drive."""
    from googleapiclient.http import MediaFileUpload

    md_files = list(BUNDLE_ROOT.rglob("*.md"))
    # Skip .git and scripts directories
    md_files = [f for f in md_files if ".git" not in str(f) and "scripts" not in str(f.parent.name)]

    existing = {f["name"]: f["id"] for f in list_drive_files(service, folder_id)}

    print(f"📤 Pushing {len(md_files)} files to Drive...")
    for local_path in md_files:
        rel_name = local_path.relative_to(BUNDLE_ROOT).as_posix()
        media = MediaFileUpload(str(local_path), mimetype="text/markdown")

        if rel_name in existing:
            # Update existing file
            service.files().update(fileId=existing[rel_name], media_body=media).execute()
            print(f"   🔄 {rel_name} (updated)")
        else:
            # Create new file
            file_metadata = {
                "name": rel_name,
                "parents": [folder_id],
                "mimeType": "text/markdown",
            }
            service.files().create(body=file_metadata, media_body=media).execute()
            print(f"   ➕ {rel_name} (created)")


def check_status(creds_data: dict):
    """Check OAuth token status."""
    expiry = creds_data.get("expiry_date")
    scopes = creds_data.get("scope", "").split(" ")
    now = datetime.now(timezone.utc).timestamp() * 1000

    print("🔐 Google OAuth Status")
    print(f"   Credentials: {CREDS_PATH}")
    print(f"   Scopes: {len(scopes)} active")
    for s in scopes:
        print(f"     - {s}")

    if expiry:
        remaining_ms = expiry - now
        remaining_min = remaining_ms / 60000
        if remaining_ms > 0:
            print(f"   Token: ✅ Valid ({remaining_min:.0f} min remaining)")
        else:
            print(f"   Token: ❌ Expired ({abs(remaining_min):.0f} min ago)")
            print("   Run: gcloud auth application-default login")
    else:
        print("   Token: ⚠️ No expiry_date in credentials")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]
    creds_data = get_credentials()

    if action == "--status":
        check_status(creds_data)
        return

    service = build_service(creds_data)
    folder_id = find_or_create_folder(service)

    if action == "--list":
        files = list_drive_files(service, folder_id)
        if files:
            print(f"\n📋 {len(files)} files in Drive:")
            for f in files:
                print(f"   {f['name']} ({f.get('size', '?')} bytes, modified {f.get('modifiedTime', '?')})")
        else:
            print("📭 No files in Drive folder.")
    elif action == "--pull":
        pull_from_drive(service, folder_id)
    elif action == "--push":
        push_to_drive(service, folder_id)
    else:
        print(f"Unknown action: {action}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()