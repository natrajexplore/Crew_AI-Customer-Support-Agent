from crewai import Crew, Process

from agents.email_classifier_agent import (
    create_email_classifier_agent,
)

from agents.email_classifier_task import (
    create_email_classifier_task,
)

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
        print("No emails found.")
        return

    message_id = messages[0]["id"]

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

    print("=" * 70)
    print("EMAIL BEING CLASSIFIED")
    print("=" * 70)
    print(customer_email[:3000])
    print("=" * 70)
    print()

    agent = create_email_classifier_agent()

    task = create_email_classifier_task(agent)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "customer_email": customer_email
        }
    )

    print()
    print("=" * 70)
    print("EMAIL CLASSIFICATION RESULT")
    print("=" * 70)
    print(result)
    print("=" * 70)


if __name__ == "__main__":
    main()

    