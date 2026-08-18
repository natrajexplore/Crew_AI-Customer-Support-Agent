from services.gmail_sender_service import (
    get_gmail_sender_service,
)

def main():

    print(
        "Starting Gmail SEND authentication..."
    )

    service = (
        get_gmail_sender_service()
    )

    print(
        "Gmail SEND authentication successful."
    )

    print()
    print(
        "Gmail API service created successfully."
    )

    print(
        "gmail.send scope is ready."
    )

    print()
    print(
        "Gmail SEND authentication test "
        "completed successfully."
    )


if __name__ == "__main__":
    main()
