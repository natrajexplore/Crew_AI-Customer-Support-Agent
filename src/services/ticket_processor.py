import os
from datetime import datetime

from dotenv import load_dotenv

from services.google_sheets_service import (
    get_google_sheets_service,
)

from services.approval_service import (
    get_approved_tickets,
    update_ticket_status,
)

from services.gmail_sender_service import (
    get_gmail_sender_service,
    send_customer_reply,
)


load_dotenv()


def process_approved_tickets():
    """
    Find human-approved tickets and send
    the approved customer responses.

    Duplicate protection:
    Only tickets whose Approval is APPROVED
    and Status is not SENT are processed.
    """

    spreadsheet_id = os.getenv(
        "GOOGLE_SHEET_ID"
    )

    if not spreadsheet_id:
        raise ValueError(
            "GOOGLE_SHEET_ID is not configured."
        )

    print()
    print("=" * 70)
    print("APPROVED TICKET PROCESSOR")
    print("=" * 70)

    # -----------------------------------------------------
    # Google Sheets
    # -----------------------------------------------------

    print("Connecting to Google Sheets...")

    sheets_service = (
        get_google_sheets_service()
    )

    print(
        "Google Sheets connection successful."
    )

    # -----------------------------------------------------
    # Find approved tickets
    # -----------------------------------------------------

    tickets = get_approved_tickets(
        sheets_service,
        spreadsheet_id,
    )

    print()
    print(
        f"Approved tickets found: "
        f"{len(tickets)}"
    )

    if not tickets:

        print(
            "No approved tickets to process."
        )

        return []

    # -----------------------------------------------------
    # Gmail SEND service
    # -----------------------------------------------------

    print()
    print(
        "Connecting to Gmail SEND service..."
    )

    gmail_service = (
        get_gmail_sender_service()
    )

    print(
        "Gmail SEND connection successful."
    )

    processed_tickets = []

    # -----------------------------------------------------
    # Process each approved ticket
    # -----------------------------------------------------

    for ticket in tickets:

        ticket_id = ticket.get(
            "Ticket ID",
            ""
        )

        customer_email = ticket.get(
            "Customer Email",
            ""
        )

        subject = ticket.get(
            "Subject",
            ""
        )

        draft_reply = ticket.get(
            "Draft Reply",
            ""
        )

        row_number = ticket.get(
            "_row_number"
        )

        print()
        print("-" * 70)
        print(
            f"Processing ticket: {ticket_id}"
        )

        print(
            f"Customer: {customer_email}"
        )

        print(
            f"Subject : {subject}"
        )

        print(
            f"Sheet row: {row_number}"
        )

        # -------------------------------------------------
        # Safety validation
        # -------------------------------------------------

        if not customer_email:

            print(
                "ERROR: Customer email is empty."
            )

            continue

        if not draft_reply:

            print(
                "ERROR: Draft reply is empty."
            )

            continue

        if not row_number:

            print(
                "ERROR: Sheet row number is missing."
            )

            continue

        try:

            # ---------------------------------------------
            # Send Gmail response
            # ---------------------------------------------

            email_response = (
                send_customer_reply(
                    service=gmail_service,
                    customer_email=customer_email,
                    subject=f"Re: {subject}",
                    body=draft_reply,
                )
            )

            gmail_message_id = (
                email_response.get(
                    "id",
                    ""
                )
            )

            print()
            print(
                "Gmail reply sent successfully."
            )

            print(
                f"Gmail Message ID: "
                f"{gmail_message_id}"
            )

            # ---------------------------------------------
            # Update Sheet
            # ---------------------------------------------

            timestamp = (
                datetime.now().isoformat(
                    timespec="seconds"
                )
            )

            update_ticket_status(
                service=sheets_service,
                spreadsheet_id=spreadsheet_id,
                row_number=row_number,
                status="SENT",
                approval_timestamp=timestamp,
                final_response=draft_reply,
            )

            print(
                "Google Sheets updated."
            )

            print(
                "Status: SENT"
            )

            processed_tickets.append(
                {
                    "ticket_id": ticket_id,
                    "gmail_message_id": (
                        gmail_message_id
                    ),
                    "status": "SENT",
                }
            )

        except Exception as error:

            print()
            print(
                "ERROR while processing ticket:"
            )

            print(error)

            # ---------------------------------------------
            # IMPORTANT:
            # Do NOT mark the ticket SENT if
            # Gmail sending failed.
            # ---------------------------------------------

            continue

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("APPROVED TICKET PROCESSING COMPLETED")
    print("=" * 70)

    print(
        f"Successfully sent: "
        f"{len(processed_tickets)}"
    )

    return processed_tickets

