import os

from dotenv import load_dotenv

from services.gmail_service import (
    get_gmail_service,
    get_message,
)

from services.google_sheets_service import (
    get_google_sheets_service,
)

from services.ticket_lookup_service import (
    is_message_already_processed,
)

from customer_support_pipeline import (
    run_customer_support_pipeline,
)


# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

CUSTOMER_EMAIL = os.getenv(
    "CUSTOMER_EMAIL",
    "angappanmuthusamy@gmail.com",
)


# ---------------------------------------------------------
# FIND CUSTOMER MESSAGES
# ---------------------------------------------------------

def find_customer_messages(
    service,
):
    """
    Find recent Gmail messages from the
    configured customer email address.
    """

    response = (
        service
        .users()
        .messages()
        .list(
            userId="me",
            q=(
                f"from:{CUSTOMER_EMAIL} "
                "newer_than:7d"
            ),
            maxResults=10,
        )
        .execute()
    )

    return response.get(
        "messages",
        [],
    )


# ---------------------------------------------------------
# PROCESS ONE GMAIL MESSAGE
# ---------------------------------------------------------

def process_gmail_message(
    gmail_service,
    sheets_service,
    spreadsheet_id,
    message_id,
):
    """
    Process one new Gmail customer message.

    Duplicate messages are skipped before
    CrewAI is called.
    """

    print()
    print("=" * 70)
    print(
        f"PROCESSING GMAIL MESSAGE: "
        f"{message_id}"
    )
    print("=" * 70)

    # -----------------------------------------------------
    # DUPLICATE CHECK
    # -----------------------------------------------------

    already_processed = (
        is_message_already_processed(
            sheets_service,
            spreadsheet_id,
            message_id,
        )
    )

    if already_processed:

        print(
            "Message already exists in "
            "Google Sheets."
        )

        print(
            "Skipping CrewAI processing."
        )

        return {
            "status": "SKIPPED",
            "reason": "ALREADY_PROCESSED",
            "message_id": message_id,
        }

    print(
        "New customer message detected."
    )

    # -----------------------------------------------------
    # READ EMAIL
    # -----------------------------------------------------

    email_data = get_message(
        gmail_service,
        message_id,
    )

    print()
    print(
        "EMAIL RECEIVED FROM GMAIL"
    )
    print("-" * 70)

    print(
        f"From    : "
        f"{email_data['sender']}"
    )

    print(
        f"Subject : "
        f"{email_data['subject']}"
    )

    print(
        f"Date    : "
        f"{email_data['date']}"
    )

    print("-" * 70)

    # -----------------------------------------------------
    # RUN AI CUSTOMER SUPPORT PIPELINE
    # -----------------------------------------------------

    result = (
        run_customer_support_pipeline(
            email_data
        )
    )

    return result


# ---------------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------------

def main():

    print()
    print("=" * 70)
    print("CUSTOMER SUPPORT AI AGENT")
    print("=" * 70)

    print()
    print(
        f"Customer filter: "
        f"{CUSTOMER_EMAIL}"
    )

    # -----------------------------------------------------
    # GOOGLE SHEETS
    # -----------------------------------------------------

    spreadsheet_id = os.getenv(
        "GOOGLE_SHEET_ID"
    )

    if not spreadsheet_id:

        raise ValueError(
            "GOOGLE_SHEET_ID is not configured "
            "in the .env file."
        )

    print()
    print(
        "Connecting to Google Sheets..."
    )

    sheets_service = (
        get_google_sheets_service()
    )

    print(
        "Google Sheets connection successful."
    )

    # -----------------------------------------------------
    # GMAIL
    # -----------------------------------------------------

    print()
    print(
        "Connecting to Gmail..."
    )

    gmail_service = (
        get_gmail_service()
    )

    print(
        "Gmail connection successful."
    )

    # -----------------------------------------------------
    # FIND CUSTOMER EMAILS
    # -----------------------------------------------------

    messages = find_customer_messages(
        gmail_service
    )

    print()
    print(
        f"Customer messages found: "
        f"{len(messages)}"
    )

    if not messages:

        print()
        print(
            "No recent customer emails found."
        )

        return

    # -----------------------------------------------------
    # PROCESS MESSAGES
    # -----------------------------------------------------

    results = []

    for message in messages:

        message_id = message["id"]

        try:

            result = (
                process_gmail_message(
                    gmail_service,
                    sheets_service,
                    spreadsheet_id,
                    message_id,
                )
            )

            results.append(result)

            print()
            print(
                "MESSAGE RESULT"
            )
            print("-" * 70)
            print(result)

        except Exception as error:

            print()
            print(
                "ERROR PROCESSING MESSAGE"
            )
            print("-" * 70)

            print(
                f"Message ID: "
                f"{message_id}"
            )

            print(
                f"Error: {error}"
            )

            results.append(
                {
                    "status": "ERROR",
                    "message_id": message_id,
                    "error": str(error),
                }
            )

            # Continue with next email
            continue

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    processed = sum(
        1
        for result in results
        if result.get("status")
        not in [
            "SKIPPED",
            "IGNORED",
        ]
    )

    skipped = sum(
        1
        for result in results
        if result.get("status")
        == "SKIPPED"
    )

    print()
    print("=" * 70)
    print("CUSTOMER SUPPORT AI AGENT COMPLETED")
    print("=" * 70)

    print(
        f"Messages found : {len(messages)}"
    )

    print(
        f"Processed       : {processed}"
    )

    print(
        f"Skipped         : {skipped}"
    )

    print("=" * 70)


# ---------------------------------------------------------
# APPLICATION ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()

    