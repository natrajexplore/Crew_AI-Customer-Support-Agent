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
        "ticket_id": "CS-HITL-TEST-001",

        "gmail_message_id": "hitl-test-message",

        "gmail_thread_id": "hitl-test-thread",

        "customer_name": "Angappan Muthusamy",

        "customer_email": "angappanmuthusamy@gmail.com",

        "subject": "Human Approval Test",

        "category": "Replacement Request",

        "priority": "Medium",

        "customer_issue": (
            "Customer received a damaged product."
        ),

        "support_analysis": (
            "Replacement requested for "
            "order ORD-45821."
        ),

        "draft_reply": (
            "Dear Angappan,\n\n"
            "We are sorry to hear that your "
            "product arrived damaged.\n\n"
            "Best regards,\n"
            "Customer Support Team"
        ),

        "status": "PENDING_REVIEW",

        "created_at": "2026-08-18 10:00:00",

        "reviewed_by": "",

        "review_notes": "",

        "approval": "PENDING",

        "approval_timestamp": "",

        "final_response": "",
    }

    response = append_ticket_row(
        service,
        spreadsheet_id,
        ticket,
    )

    updated_range = (
        response
        .get("updates", {})
        .get(
            "updatedRange",
            "Unknown"
        )
    )

    print()
    print("Human approval test ticket created.")
    print(
        f"Updated range: {updated_range}"
    )


if __name__ == "__main__":
    main()

    