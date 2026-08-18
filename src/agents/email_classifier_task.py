from crewai import Task


def create_email_classifier_task(agent):

    task = Task(
        description=(
            "Classify the following incoming email.\n\n"

            "EMAIL:\n"
            "{customer_email}\n\n"

            "Determine whether this is a genuine customer support "
            "request that should enter the customer support workflow.\n\n"

            "Return exactly the following fields:\n\n"
            "IS_CUSTOMER_SUPPORT: YES or NO\n"
            "CATEGORY: one of the following categories or OTHER\n"
            "CONFIDENCE: HIGH, MEDIUM, or LOW\n"
            "REASON: one short explanation\n\n"

            "Customer support examples include:\n"
            "- Product questions\n"
            "- Order issues\n"
            "- Delivery problems\n"
            "- Refund requests\n"
            "- Replacement requests\n"
            "- Billing questions\n"
            "- Account problems\n"
            "- Complaints\n"
            "- Technical support requests\n\n"

            "Non-support examples include:\n"
            "- Newsletters\n"
            "- Marketing emails\n"
            "- Advertisements\n"
            "- Social-network notifications\n"
            "- LinkedIn connection invitations\n"
            "- Promotional campaigns\n"
            "- Unrelated personal emails\n\n"

            "Important rules:\n"
            "- Do not invent information.\n"
            "- Classify based only on the email content.\n"
            "- A sender mentioning a product or company does not by "
            "itself make an email a support request.\n"
            "- When uncertain, explain why."
        ),
        expected_output=(
            "IS_CUSTOMER_SUPPORT: YES or NO\n"
            "CATEGORY: category\n"
            "CONFIDENCE: HIGH, MEDIUM, or LOW\n"
            "REASON: short explanation"
        ),
        agent=agent,
    )

    return task

