from crewai import Task


def create_customer_analysis_task(agent):

    return Task(
        description="""
Analyze the customer support email and provide a structured
support analysis for the customer service team.

CUSTOMER EMAIL:
{customer_email}

Analyze the email and identify:

1. Customer name
2. Customer email
3. Order number, if available
4. Customer issue
5. Issue category
6. Priority
7. Important details provided by the customer
8. Recommended support action

Requirements:

- Carefully read the complete customer email.
- Identify the customer's actual problem.
- Extract the order number if one is present.
- Do not invent information that is not present in the email.
- Do not assume policies, refunds, replacement dates, or guarantees
  unless they are explicitly provided.
- Use "Not provided" when information is unavailable.
- Be concise and professional.
- This is an internal support analysis.
- Do not write a customer-facing email response.
- Do not include an email signature.

Return the analysis in the following format:

Customer Name:
Customer Email:
Order Number:
Issue:
Category:
Priority:
Important Details:
Recommended Action:
""",

        expected_output="""
A structured internal customer-support analysis containing:

Customer Name
Customer Email
Order Number
Issue
Category
Priority
Important Details
Recommended Action

Do not generate a customer-facing email.
""",

        agent=agent,
    )

