import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_gmail_service():
    # Load secrets from environment variables
    client_id = os.environ["GMAIL_CLIENT_ID"]
    client_secret = os.environ["GMAIL_CLIENT_SECRET"]
    refresh_token = os.environ["GMAIL_REFRESH_TOKEN"]

    # Create credentials object using refresh token
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token"
    )

    # Build Gmail API client
    return build("gmail", "v1", credentials=creds)

def list_inbox_messages():
    service = get_gmail_service()

    # Fetch messages
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=10
    ).execute()

    messages = results.get("messages", [])

    # Print message snippets
    for m in messages:
        msg = service.users().messages().get(userId="me", id=m["id"]).execute()
        print(f"ID: {m['id']}")
        print(f"Snippet: {msg.get('snippet', '')}")
        print("-" * 40)

if __name__ == "__main__":
    list_inbox_messages()
