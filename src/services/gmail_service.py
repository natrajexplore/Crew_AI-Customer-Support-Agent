import base64
from email import message_from_bytes
from email.utils import parseaddr
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


# ---------------------------------------------------------
# GMAIL READ SCOPE
# ---------------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


# ---------------------------------------------------------
# GMAIL AUTHENTICATION
# ---------------------------------------------------------

def get_gmail_service():
    """
    Authenticate the user and return an authenticated
    Gmail API service.
    """

    credentials = None

    # -----------------------------------------------------
    # Reuse existing token
    # -----------------------------------------------------

    if TOKEN_FILE.exists():

        credentials = (
            Credentials.from_authorized_user_file(
                str(TOKEN_FILE),
                SCOPES
            )
        )

    # -----------------------------------------------------
    # Authenticate if required
    # -----------------------------------------------------

    if not credentials or not credentials.valid:

        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):

            credentials.refresh(
                Request()
            )

        else:

            if not CREDENTIALS_FILE.exists():

                raise FileNotFoundError(
                    f"credentials.json not found at: "
                    f"{CREDENTIALS_FILE}"
                )

            flow = (
                InstalledAppFlow
                .from_client_secrets_file(
                    str(CREDENTIALS_FILE),
                    SCOPES
                )
            )

            credentials = (
                flow.run_local_server(
                    port=0
                )
            )

        # -------------------------------------------------
        # Save token
        # -------------------------------------------------

        with open(
            TOKEN_FILE,
            "w",
            encoding="utf-8"
        ) as token:

            token.write(
                credentials.to_json()
            )

    # -----------------------------------------------------
    # Create Gmail API service
    # -----------------------------------------------------

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return service


# ---------------------------------------------------------
# LIST UNREAD GMAIL MESSAGES
# ---------------------------------------------------------

def list_recent_messages(
    service,
    max_results=10
):
    """
    Retrieve unread messages from the Gmail inbox.

    Only unread inbox messages are returned so that
    the customer-support pipeline does not repeatedly
    process previously handled emails.
    """

    response = (
        service
        .users()
        .messages()
        .list(
            userId="me",
            labelIds=["INBOX"],
            q="is:unread",
            maxResults=max_results
        )
        .execute()
    )

    messages = response.get(
        "messages",
        []
    )

    return messages


# ---------------------------------------------------------
# GET AND PARSE GMAIL MESSAGE
# ---------------------------------------------------------

def get_message(
    service,
    message_id
):
    """
    Retrieve and parse a Gmail message.

    Returns:
        message_id
        thread_id
        sender
        customer_name
        customer_email
        subject
        date
        body
    """

    message = (
        service
        .users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="raw"
        )
        .execute()
    )

    # -----------------------------------------------------
    # Decode raw Gmail message
    # -----------------------------------------------------

    raw_message = (
        base64.urlsafe_b64decode(
            message["raw"]
        )
    )

    email_message = (
        message_from_bytes(
            raw_message
        )
    )

    # -----------------------------------------------------
    # Read email headers
    # -----------------------------------------------------

    sender = email_message.get(
        "From",
        ""
    )

    subject = email_message.get(
        "Subject",
        ""
    )

    date = email_message.get(
        "Date",
        ""
    )

    # -----------------------------------------------------
    # Parse customer name and email
    # -----------------------------------------------------

    customer_name, customer_email = (
        parseaddr(sender)
    )

    # -----------------------------------------------------
    # Extract email body
    # -----------------------------------------------------

    body = extract_email_body(
        email_message
    )

    # -----------------------------------------------------
    # Return structured email data
    # -----------------------------------------------------

    return {
        "message_id": message["id"],
        "thread_id": message["threadId"],
        "sender": sender,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "subject": subject,
        "date": date,
        "body": body,
    }


# ---------------------------------------------------------
# EXTRACT EMAIL BODY
# ---------------------------------------------------------

def extract_email_body(
    email_message
):
    """
    Extract readable text from an email message.
    """

    body = ""

    # -----------------------------------------------------
    # Multipart email
    # -----------------------------------------------------

    if email_message.is_multipart():

        for part in email_message.walk():

            content_type = (
                part.get_content_type()
            )

            content_disposition = str(
                part.get(
                    "Content-Disposition",
                    ""
                )
            )

            if (
                content_type == "text/plain"
                and "attachment"
                not in content_disposition
            ):

                payload = part.get_payload(
                    decode=True
                )

                if payload:

                    body = payload.decode(
                        "utf-8",
                        errors="replace"
                    )

                    break

    # -----------------------------------------------------
    # Simple email
    # -----------------------------------------------------

    else:

        payload = email_message.get_payload(
            decode=True
        )

        if payload:

            body = payload.decode(
                "utf-8",
                errors="replace"
            )

    return body.strip()
