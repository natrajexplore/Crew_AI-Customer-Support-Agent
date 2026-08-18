import os

from dotenv import load_dotenv

from services.google_sheets_service import (
    get_google_sheets_service,
)

from services.approval_service import (
    get_approved_tickets,
)


load_dotenv()


def main():

    spreadsheet_id = os.getenv(
        "GOOGLE_SHEET_ID"
    )

    if not spreadsheet_id:
        raise ValueError(
            "GOOGLE_SHEET_ID is not configured."
        )

    print()
    print("=" * 70)
    print("TICKET PROCESSOR DRY RUN")
    print("=" * 70)

    service = (
        get_google_sheets_service()
    )

    tickets = get_approved_tickets(
        service,
        spreadsheet_id,
    )

    print()
    print(
        f"Approved tickets found: "
        f"{len(tickets)}"
    )

    for ticket in tickets:

        print()
        print("-" * 70)

        print(
            f"Ticket ID : "
            f"{ticket.get('Ticket ID')}"
        )

        print(
            f"Customer  : "
            f"{ticket.get('Customer Name')}"
        )

        print(
            f"Email     : "
            f"{ticket.get('Customer Email')}"
        )

        print(
            f"Subject   : "
            f"{ticket.get('Subject')}"
        )

        print(
            f"Status    : "
            f"{ticket.get('Status')}"
        )

        print(
            f"Approval  : "
            f"{ticket.get('Approval')}"
        )

        print()
        print("DRAFT RESPONSE:")
        print("-" * 70)

        print(
            ticket.get(
                "Draft Reply",
                ""
            )
        )

        print("-" * 70)

        print(
            "DRY RUN: NO EMAIL SENT."
        )

    print()
    print("=" * 70)
    print(
        "DRY RUN COMPLETED"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()

    