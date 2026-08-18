import base64
from email.mime.text import MIMEText
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
TOKEN_FILE = BASE_DIR / "gmail_send_token.json"


# ---------------------------------------------------------
# GMAIL SEND SCOPE
# ---------------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


# ---------------------------------------------------------
# CUSTOMER SUPPORT EMAIL SIGNATURE
# ---------------------------------------------------------

EMAIL_SIGNATURE = """[Maddy]
Explore Customer Support Team
[Explore-AI]
[9999900000]"""


# ---------------------------------------------------------
# GMAIL AUTHENTICATION
# ---------------------------------------------------------

def get_gmail_sender_service():
    """
    Authenticate Gmail with send permission
    and return the Gmail API service.
    """

    credentials = None

    # -----------------------------------------------------
    # Reuse existing send token
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
        # Save send token
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
# BUILD CUSTOMER EMAIL BODY
# ---------------------------------------------------------

def build_customer_email_body(
    body
):
    """
    Add the standard Explore-AI customer-support
    signature to the AI-generated response.
    """

    clean_body = (
        str(body)
        .strip()
    )

    if not clean_body:
        clean_body = (
            "Thank you for contacting "
            "Customer Support."
        )

    final_body = (
        clean_body
        + "\n\n"
        + EMAIL_SIGNATURE
    )

    return final_body


# ---------------------------------------------------------
# SEND CUSTOMER REPLY
# ---------------------------------------------------------

def send_customer_reply(
    service,
    customer_email,
    subject,
    body,
    thread_id=None,
    in_reply_to=None,
):
    """
    Send a customer-support reply.

    The AI-generated response is automatically
    appended with the standard customer-support
    signature.

    If thread_id is provided, Gmail associates
    the message with the existing conversation.
    """

    # -----------------------------------------------------
    # Build final email body
    # -----------------------------------------------------

    final_body = build_customer_email_body(
        body
    )

    # -----------------------------------------------------
    # Create MIME message
    # -----------------------------------------------------

    message = MIMEText(
        final_body,
        "plain",
        "utf-8",
    )

    # -----------------------------------------------------
    # Email headers
    # -----------------------------------------------------

    message["To"] = customer_email
    message["Subject"] = subject

    # -----------------------------------------------------
    # Preserve Gmail conversation/thread
    # -----------------------------------------------------

    if in_reply_to:

        message["In-Reply-To"] = (
            in_reply_to
        )

        message["References"] = (
            in_reply_to
        )

    # -----------------------------------------------------
    # Encode message for Gmail API
    # -----------------------------------------------------

    encoded_message = (
        base64.urlsafe_b64encode(
            message.as_bytes()
        )
        .decode("utf-8")
    )

    # -----------------------------------------------------
    # Gmail API request
    # -----------------------------------------------------

    request_body = {
        "raw": encoded_message
    }

    if thread_id:

        request_body["threadId"] = (
            thread_id
        )

    # -----------------------------------------------------
    # Send email
    # -----------------------------------------------------

    response = (
        service
        .users()
        .messages()
        .send(
            userId="me",
            body=request_body,
        )
        .execute()
    )

    return response
