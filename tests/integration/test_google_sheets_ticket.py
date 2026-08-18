import os

from dotenv import load_dotenv

from services.google_sheets_service import (
    get_google_sheets_service,
    append_ticket_row,
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

    print("Connecting to Google Sheets...")

    service = get_google_sheets_service()

    print("Google Sheets connection successful.")

    ticket = {
        "ticket_id": "CS-TEST-001",
        "gmail_message_id": "test-gmail-001",
        "gmail_thread_id": "test-thread-001",
        "customer_name": "Angappan Muthusamy",
        "customer_email": "angappanmuthusamy@gmail.com",
        "subject": "Damaged Product - Replacement Request",
        "category": "Replacement Request",
        "priority": "Medium",
        "customer_issue": (
            "Customer received a damaged product "
            "and requested a replacement."
        ),
        "support_analysis": (
            "Order ORD-45821 reported as damaged. "
            "Replacement requested."
        ),
        "draft_reply": (
            "Dear Angappan,\n\n"
            "We are sorry to hear that your order "
            "arrived damaged. We will review your "
            "replacement request and provide the "
            "next steps.\n\n"
            "Best regards,\n"
            "Customer Support Team"
        ),
        "status": "PENDING_REVIEW",
        "created_at": "2026-08-18 09:00:00",
        "reviewed_by": "",
        "review_notes": "",
    }

    response = append_ticket_row(
        service,
        spreadsheet_id,
        ticket,
    )

    updated_range = (
        response
        .get("updates", {})
        .get("updatedRange", "Unknown")
    )

    print()
    print("Ticket inserted successfully.")
    print(f"Updated range: {updated_range}")


if __name__ == "__main__":
    main()

    