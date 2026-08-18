import os

from dotenv import load_dotenv

from services.google_sheets_service import (
    get_google_sheets_service,
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
    print()

    response = (
        service
        .spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="Tickets!A:R",
        )
        .execute()
    )

    rows = response.get(
        "values",
        []
    )

    print("=" * 100)
    print("GOOGLE SHEETS DATA")
    print("=" * 100)

    if not rows:
        print("No rows found.")
        return

    for row_number, row in enumerate(
        rows,
        start=1,
    ):

        print()
        print(
            f"ROW {row_number}"
        )
        print("-" * 100)

        for column_number, value in enumerate(
            row,
            start=1,
        ):

            print(
                f"Column {column_number:02d}: "
                f"{value!r}"
            )

    print()
    print("=" * 100)


if __name__ == "__main__":
    main()
    