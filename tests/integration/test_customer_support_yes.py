from crewai import Crew, Process

from agents.email_classifier_agent import (
    create_email_classifier_agent,
)

from agents.email_classifier_task import (
    create_email_classifier_task,
)

from agents.customer_support_agent import (
    create_customer_support_agent,
)

from agents.customer_support_task import (
    create_customer_analysis_task,
)

from agents.response_generator_agent import (
    create_response_generator_agent,
)

from agents.response_generator_task import (
    create_response_generator_task,
)

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

    if not messages:

        print(
            f"No messages found from {sender}"
        )

        return

    # Use the most recent email from the test customer
    message_id = messages[0]["id"]

    print(
        f"Processing customer message: {message_id}"
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
    print("CUSTOMER EMAIL")
    print("=" * 70)

    print(customer_email)

    print("=" * 70)

    # ---------------------------------------------------------
    # STEP 1 - CLASSIFIER
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 1: EMAIL CLASSIFICATION")
    print("=" * 70)

    classifier_agent = create_email_classifier_agent()

    classifier_task = create_email_classifier_task(
        classifier_agent
    )

    classifier_crew = Crew(
        agents=[classifier_agent],
        tasks=[classifier_task],
        process=Process.sequential,
        verbose=True,
    )

    classification = classifier_crew.kickoff(
        inputs={
            "customer_email": customer_email
        }
    )

    classification_text = str(classification)

    print()
    print("CLASSIFICATION")
    print("-" * 70)
    print(classification_text)
    print("-" * 70)

    # ---------------------------------------------------------
    # CHECK CLASSIFICATION
    # ---------------------------------------------------------

    if "IS_CUSTOMER_SUPPORT: YES" not in (
        classification_text.upper()
    ):

        print()
        print("=" * 70)
        print("EMAIL WAS CLASSIFIED AS NON-SUPPORT")
        print("=" * 70)

        print(
            "The AI correctly stopped the workflow."
        )

        return

    # ---------------------------------------------------------
    # STEP 2 - SUPPORT ANALYSIS
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 2: CUSTOMER SUPPORT ANALYSIS")
    print("=" * 70)

    support_agent = create_customer_support_agent()

    support_task = create_customer_analysis_task(
        support_agent
    )

    support_crew = Crew(
        agents=[support_agent],
        tasks=[support_task],
        process=Process.sequential,
        verbose=True,
    )

    support_analysis = support_crew.kickoff(
        inputs={
            "customer_email": customer_email
        }
    )

    print()
    print("SUPPORT ANALYSIS")
    print("-" * 70)
    print(support_analysis)
    print("-" * 70)

    # ---------------------------------------------------------
    # STEP 3 - RESPONSE GENERATION
    # ---------------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 3: RESPONSE GENERATION")
    print("=" * 70)

    response_agent = create_response_generator_agent()

    response_task = create_response_generator_task(
        response_agent
    )

    response_crew = Crew(
        agents=[response_agent],
        tasks=[response_task],
        process=Process.sequential,
        verbose=True,
    )

    draft_response = response_crew.kickoff(
        inputs={
            "customer_email": customer_email,
            "support_analysis": str(support_analysis),
        }
    )

    print()
    print("=" * 70)
    print("CUSTOMER RESPONSE DRAFT")
    print("=" * 70)
    print(draft_response)
    print("=" * 70)


if __name__ == "__main__":
    main()

    