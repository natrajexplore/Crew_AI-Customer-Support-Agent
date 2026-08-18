from crewai import Crew, Process

from agents.customer_support_agent import (
    create_customer_support_agent,
)

from agents.customer_support_task import (
    create_customer_analysis_task,
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
        print("No emails found in the inbox.")
        return

    message_id = messages[0]["id"]

    print(f"Processing Gmail message: {message_id}")
    print()

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
    print("CUSTOMER EMAIL")
    print("=" * 70)
    print(customer_email[:3000])
    print("=" * 70)
    print()

    print("Creating Customer Support Agent...")

    agent = create_customer_support_agent()

    task = create_customer_analysis_task(agent)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    print("Sending Gmail email to CrewAI...")
    print()

    result = crew.kickoff(
        inputs={
            "customer_email": customer_email,
        }
    )

    print()
    print("=" * 70)
    print("AI CUSTOMER SUPPORT ANALYSIS")
    print("=" * 70)
    print(result)
    print("=" * 70)


if __name__ == "__main__":
    main()


    