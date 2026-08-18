
import customer_support_pipeline as pipeline

from services.gmail_service import (
    get_gmail_service,
    list_recent_messages,
    get_message,
)

def main():

    print("Connecting to Gmail...")

    service = get_gmail_service()

    print("Gmail connection successful.")
    print()

    messages = list_recent_messages(
        service,
        max_results=1,
    )

    if not messages:

        print("No Gmail messages found.")

        return

    message_id = messages[0]["id"]

    print(
        f"Processing Gmail message: {message_id}"
    )

    email_data = get_message(
        service,
        message_id,
    )

    customer_email = f"""
From: {email_data['sender']}
Subject: {email_data['subject']}
Date: {email_data['date']}

{email_data['body']}
"""

    print()
    print("=" * 70)
    print("EMAIL RECEIVED FROM GMAIL")
    print("=" * 70)

    print(customer_email[:3000])

    print("=" * 70)

    result = pipeline.run_customer_support_pipeline(
    customer_email
    )

    print()
    print("=" * 70)
    print("FINAL PIPELINE RESULT")
    print("=" * 70)

    print(result)

    print("=" * 70)


if __name__ == "__main__":
    main()


