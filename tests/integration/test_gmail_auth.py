from services.gmail_service import get_gmail_service

def main():
    print("Starting Gmail authentication...")

    service = get_gmail_service()

    print("Gmail authentication successful!")

    # Get Gmail profile information
    profile = (
        service.users()
        .getProfile(userId="me")
        .execute()
    )

    print()
    print("Authenticated Gmail account:")
    print(profile["emailAddress"])

    print()
    print("Authentication test completed successfully.")


if __name__ == "__main__":
    main()
    

