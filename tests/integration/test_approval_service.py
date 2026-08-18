import os

from dotenv import load_dotenv

from services.google_sheets_service import (
    get_google_sheets_service,
)

from services.approval_service import (
    get_approved_tickets,
)


def main():

    load_dotenv()

    spreadsheet_id = os.getenv(
        "GOOGLE_SHEET_ID"
    )

    if not spreadsheet_id:

        raise ValueError(
            "GOOGLE_SHEET_ID is not configured."
        )

    print(
        "Connecting to Google Sheets..."
    )

    service = (
        get_google_sheets_service()
    )

    print(
        "Google Sheets connection successful."
    )

    print()
    print(
        "Checking for approved tickets..."
    )

    tickets = get_approved_tickets(
        service,
        spreadsheet_id,
    )

    print()
    print("=" * 70)
    print(
        f"APPROVED TICKETS FOUND: "
        f"{len(tickets)}"
    )
    print("=" * 70)

    for ticket in tickets:

        print()
        print(
            f"Ticket ID : "
            f"{ticket.get('Ticket ID', '')}"
        )

        print(
            f"Customer  : "
            f"{ticket.get('Customer Name', '')}"
        )

        print(
            f"Email     : "
            f"{ticket.get('Customer Email', '')}"
        )

        print(
            f"Subject   : "
            f"{ticket.get('Subject', '')}"
        )

        print(
            f"Approval  : "
            f"{ticket.get('Approval', '')}"
        )

        print(
            f"Status    : "
            f"{ticket.get('Status', '')}"
        )

        print("-" * 70)


if __name__ == "__main__":
    main()

    