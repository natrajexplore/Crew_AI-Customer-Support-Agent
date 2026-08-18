import os

from dotenv import load_dotenv

from services.google_sheets_service import (
    get_google_sheets_service,
)

from services.ticket_lookup_service import (
    get_processed_message_ids,
    is_message_already_processed,
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

    # -----------------------------------------------------
    # Get existing message IDs
    # -----------------------------------------------------

    processed_ids = (
        get_processed_message_ids(
            service,
            spreadsheet_id,
        )
    )

    print()
    print(
        f"Processed Gmail Message IDs: "
        f"{len(processed_ids)}"
    )

    for message_id in processed_ids:

        print(
            f"  - {message_id}"
        )

    # -----------------------------------------------------
    # Test an existing message
    # -----------------------------------------------------

    test_message_id = (
        "test-gmail-001"
    )

    result = (
        is_message_already_processed(
            service,
            spreadsheet_id,
            test_message_id,
        )
    )

    print()
    print(
        f"Test Message ID: "
        f"{test_message_id}"
    )

    print(
        f"Already processed: "
        f"{result}"
    )

    # -----------------------------------------------------
    # Test a new message
    # -----------------------------------------------------

    new_message_id = (
        "brand-new-message-999"
    )

    result = (
        is_message_already_processed(
            service,
            spreadsheet_id,
            new_message_id,
        )
    )

    print()
    print(
        f"Test Message ID: "
        f"{new_message_id}"
    )

    print(
        f"Already processed: "
        f"{result}"
    )


if __name__ == "__main__":
    main()

