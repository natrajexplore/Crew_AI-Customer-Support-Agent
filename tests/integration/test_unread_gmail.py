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
        max_results=10,
    )

    print(f"Unread messages found: {len(messages)}")
    print("=" * 70)

    if not messages:
        print("No unread messages found.")
        return

    for index, message in enumerate(messages, start=1):

        message_id = message["id"]

        email_data = get_message(
            service,
            message_id,
        )

        print()
        print(f"EMAIL #{index}")
        print("-" * 70)
        print(f"Message ID : {message_id}")
        print(f"From       : {email_data['sender']}")
        print(f"Subject    : {email_data['subject']}")
        print(f"Date       : {email_data['date']}")
        print("-" * 70)


if __name__ == "__main__":
    main()

    