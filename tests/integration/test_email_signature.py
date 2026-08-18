from services.gmail_sender_service import (
    build_customer_email_body,
)


def main():

    draft_reply = """Dear Angappan,

We are sorry to hear that your order arrived damaged.

We will review your replacement request and provide the next steps.

Best regards,
Customer Support Team"""

    final_body = build_customer_email_body(
        draft_reply
    )

    print()
    print("=" * 70)
    print("FINAL CUSTOMER EMAIL")
    print("=" * 70)
    print()
    print(final_body)
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

    