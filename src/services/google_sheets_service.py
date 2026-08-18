from datetime import datetime
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

TOKEN_FILE = BASE_DIR / "sheets_token.json"


# ---------------------------------------------------------
# GOOGLE SHEETS SCOPE
# ---------------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


# ---------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------

def get_google_sheets_service():
    """
    Authenticate with Google and return
    an authenticated Google Sheets API service.
    """

    credentials = None

    # -----------------------------------------------------
    # Reuse existing OAuth token
    # -----------------------------------------------------

    if TOKEN_FILE.exists():

        credentials = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )

    # -----------------------------------------------------
    # Authenticate if credentials are missing/invalid
    # -----------------------------------------------------

    if not credentials or not credentials.valid:

        # -------------------------------------------------
        # Refresh existing credentials
        # -------------------------------------------------

        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):

            credentials.refresh(Request())

        # -------------------------------------------------
        # Start new OAuth flow
        # -------------------------------------------------

        else:

            if not CREDENTIALS_FILE.exists():

                raise FileNotFoundError(
                    f"credentials.json not found at: "
                    f"{CREDENTIALS_FILE}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES
            )

            credentials = flow.run_local_server(
                port=0
            )

        # -------------------------------------------------
        # Save credentials for future use
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
    # Create Google Sheets API client
    # -----------------------------------------------------

    service = build(
        "sheets",
        "v4",
        credentials=credentials
    )

    return service


# ---------------------------------------------------------
# APPEND TICKET ROW
# ---------------------------------------------------------

def append_ticket_row(
    service,
    spreadsheet_id,
    ticket_data,
):
    """
    Append one customer-support ticket
    to the Tickets worksheet.

    Columns:
    A - Ticket ID
    B - Gmail Message ID
    C - Gmail Thread ID
    D - Customer Name
    E - Customer Email
    F - Subject
    G - Category
    H - Priority
    I - Customer Issue
    J - Support Analysis
    K - Draft Reply
    L - Status
    M - Created At
    N - Reviewed By
    O - Review Notes
    P - Approval
    Q - Approval Timestamp
    R - Final Response
    """

    row = [
        ticket_data.get("ticket_id", ""),

        ticket_data.get(
            "gmail_message_id",
            ""
        ),

        ticket_data.get(
            "gmail_thread_id",
            ""
        ),

        ticket_data.get(
            "customer_name",
            ""
        ),

        ticket_data.get(
            "customer_email",
            ""
        ),

        ticket_data.get(
            "subject",
            ""
        ),

        ticket_data.get(
            "category",
            ""
        ),

        ticket_data.get(
            "priority",
            ""
        ),

        ticket_data.get(
            "customer_issue",
            ""
        ),

        ticket_data.get(
            "support_analysis",
            ""
        ),

        ticket_data.get(
            "draft_reply",
            ""
        ),

        ticket_data.get(
            "status",
            "PENDING_REVIEW"
        ),

        ticket_data.get(
            "created_at",
            ""
        ),

        ticket_data.get(
            "reviewed_by",
            ""
        ),

        ticket_data.get(
            "review_notes",
            ""
        ),

        ticket_data.get(
            "approval",
            "PENDING"
        ),

        ticket_data.get(
            "approval_timestamp",
            ""
        ),

        ticket_data.get(
            "final_response",
            ""
        ),
    ]

    # -----------------------------------------------------
    # Append row to Google Sheets
    # -----------------------------------------------------

    response = (
        service
        .spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range="Tickets!A:R",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={
                "values": [row]
            },
        )
        .execute()
    )

    return response


# ---------------------------------------------------------
# CREATE SUPPORT TICKET
# ---------------------------------------------------------

def create_support_ticket(
    spreadsheet_id,
    customer_email,
    support_analysis,
    draft_reply,
    classification,
):
    """
    Create a customer-support ticket
    and save it to Google Sheets.

    New tickets are created with:

        Status   = PENDING_REVIEW
        Approval = PENDING
    """

    # -----------------------------------------------------
    # Get authenticated Sheets service
    # -----------------------------------------------------

    service = get_google_sheets_service()

    # -----------------------------------------------------
    # Generate ticket ID
    # -----------------------------------------------------

    ticket_id = (
        "CS-"
        + datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )
    )

    # -----------------------------------------------------
    # Build ticket data
    # -----------------------------------------------------

    ticket_data = {

        "ticket_id": ticket_id,

        "gmail_message_id": (
            customer_email.get(
                "message_id",
                ""
            )
        ),

        "gmail_thread_id": (
            customer_email.get(
                "thread_id",
                ""
            )
        ),

        "customer_name": (
            customer_email.get(
                "customer_name",
                ""
            )
        ),

       "customer_email": 
            customer_email.get(
               "customer_email",
          ""
        ),

        "subject": (
            customer_email.get(
                "subject",
                ""
            )
        ),

        "category": classification,

        "priority": "",

        "customer_issue": "",

        "support_analysis": str(
            support_analysis
        ),

        "draft_reply": str(
            draft_reply
        ),

        "status": "PENDING_REVIEW",

        "created_at": (
            datetime.now().isoformat(
                timespec="seconds"
            )
        ),

        "reviewed_by": "",

        "review_notes": "",

        "approval": "PENDING",

        "approval_timestamp": "",

        "final_response": "",
    }

    # -----------------------------------------------------
    # Insert ticket into Google Sheets
    # -----------------------------------------------------

    response = append_ticket_row(
        service=service,
        spreadsheet_id=spreadsheet_id,
        ticket_data=ticket_data,
    )

    # -----------------------------------------------------
    # Get updated range
    # -----------------------------------------------------

    updated_range = (
        response
        .get("updates", {})
        .get(
            "updatedRange",
            "Unknown"
        )
    )

    # -----------------------------------------------------
    # Return ticket information
    # -----------------------------------------------------

    return {
        "ticket_id": ticket_id,

        "status": "PENDING_REVIEW",

        "approval": "PENDING",

        "updated_range": updated_range,
    }

