from crewai import Task


def create_response_generator_task(agent):

    task = Task(
        description=(
            "Write a professional customer support email response.\n\n"

            "CUSTOMER EMAIL:\n"
            "{customer_email}\n\n"

            "SUPPORT ANALYSIS:\n"
            "{support_analysis}\n\n"

            "Requirements:\n"
            "- Address the customer's actual issue.\n"
            "- Be professional and empathetic.\n"
            "- Do not invent company policies.\n"
            "- Do not invent refund amounts, replacement dates, "
            "shipping dates, or guarantees.\n"
            "- Do not claim that an action has already been completed "
            "unless the analysis explicitly confirms it.\n"
            "- If information or action is required from the customer, "
            "clearly explain it.\n"
            "- Keep the response concise.\n"
            "- Do not include internal AI analysis in the customer reply.\n"
            "- Return only the email draft."
        ),
        expected_output=(
            "A professional customer-facing email containing:\n"
            "- Greeting\n"
            "- Clear response to the customer's issue\n"
            "- Appropriate next steps\n"
            "- Professional closing"
        ),
        agent=agent,
    )

    return task

