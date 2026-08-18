from services.gmail_service import (
    get_gmail_service,
    get_message,
)


def main():

    print(
        "Connecting to Gmail..."
    )

    service = get_gmail_service()

    print(
        "Gmail connection successful."
    )

    print()

    response = (
        service.users()
        .messages()
        .list(
            userId="me",
            q="from:angappanmuthusamy@gmail.com",
            maxResults=1,
        )
        .execute()
    )

    messages = response.get(
        "messages",
        []
    )

    if not messages:

        print(
            "No customer email found."
        )

        return

    message_id = messages[0]["id"]

    email_data = get_message(
        service,
        message_id,
    )

    print()
    print("=" * 70)
    print("CUSTOMER EMAIL PARSER TEST")
    print("=" * 70)

    print(
        f"Original From : "
        f"{email_data['sender']}"
    )

    print(
        f"Customer Name : "
        f"{email_data['customer_name']}"
    )

    print(
        f"Customer Email: "
        f"{email_data['customer_email']}"
    )

    print(
        f"Subject       : "
        f"{email_data['subject']}"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()

    