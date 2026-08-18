from services.google_sheets_service import get_google_sheets_service

from dotenv import load_dotenv
import os


def main():

    print("Starting Google Sheets authentication...")

    load_dotenv()

    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")

    if not spreadsheet_id:
        raise ValueError(
            "GOOGLE_SHEET_ID is not configured in .env"
        )

    print("Spreadsheet ID found.")

    service = get_google_sheets_service()

    print("Google Sheets authentication successful.")
    print()

    # Test row
    test_row = [
        "TEST-001",
        "test-message-id",
        "test-thread-id",
        "Angappan Muthusamy",
        "angappanmuthusamy@gmail.com",
        "Test Customer Support Ticket",
        "Test",
        "Low",
        "This is a Google Sheets integration test.",
        "Test analysis",
        "This is a test response.",
        "TEST",
        "2026-08-18",
        "",
        "",
    ]

    response = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range="Tickets!A:O",
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={
                "values": [test_row]
            },
        )
        .execute()
    )

    print("Test row inserted successfully.")
    print()
    print("Updated range:")
    print(
        response.get(
            "updates",
            {}
        ).get(
            "updatedRange",
            "Unknown"
        )
    )


if __name__ == "__main__":
    main()


