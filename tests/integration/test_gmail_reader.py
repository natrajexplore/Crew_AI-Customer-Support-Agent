from services.gmail_service import (
    get_gmail_service,
    list_recent_messages,
    get_message,
)

def main():

    print("Connecting to Gmail...")

    service = get_gmail_service()

    print("Connected successfully.")
    print()

    messages = list_recent_messages(
        service,
        max_results=5
    )

    if not messages:
        print("No messages found in the inbox.")
        return

    print(f"Found {len(messages)} messages.")
    print("=" * 70)

    for message in messages:

        email_data = get_message(
            service,
            message["id"]
        )

        print()
        print(f"Message ID : {email_data['message_id']}")
        print(f"Thread ID  : {email_data['thread_id']}")
        print(f"From       : {email_data['sender']}")
        print(f"Subject    : {email_data['subject']}")
        print(f"Date       : {email_data['date']}")

        print("-" * 70)

        print("Body:")
        print(email_data["body"][:1000])

        print("=" * 70)


if __name__ == "__main__":
    main()

