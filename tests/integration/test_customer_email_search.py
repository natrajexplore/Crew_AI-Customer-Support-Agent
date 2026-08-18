
from services.gmail_service import (
    get_gmail_service,
    get_message,
)


def main():

    print("Connecting to Gmail...")

    service = get_gmail_service()

    print("Gmail connection successful.")
    print()

    sender = "angappanmuthusamy@gmail.com"

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=f"from:{sender}",
            maxResults=10,
        )
        .execute()
    )

    messages = response.get("messages", [])

    print(
        f"Messages found from {sender}: {len(messages)}"
    )

    print("=" * 70)

    if not messages:

        print()
        print("No email from Angappan was found.")
        print()
        print("Please verify:")
        print("1. The email was actually sent.")
        print("2. The recipient address is correct.")
        print("3. Check Gmail Spam.")
        print("4. Check Gmail All Mail.")
        return

    for index, message in enumerate(
        messages,
        start=1,
    ):

        message_id = message["id"]

        email_data = get_message(
            service,
            message_id,
        )

        print()
        print(f"EMAIL #{index}")
        print("-" * 70)
        print(
            f"Message ID : "
            f"{email_data['message_id']}"
        )
        print(
            f"From       : "
            f"{email_data['sender']}"
        )
        print(
            f"Subject    : "
            f"{email_data['subject']}"
        )
        print(
            f"Date       : "
            f"{email_data['date']}"
        )
        print("-" * 70)


if __name__ == "__main__":
    main()

    