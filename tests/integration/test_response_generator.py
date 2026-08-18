from crewai import Crew, Process

from agents.response_generator_agent import (
    create_response_generator_agent,
)

from agents.response_generator_task import (
    create_response_generator_task,
)


def main():

    customer_email = """
    From: angappanmuthusamy@gmail.com

    Subject: Damaged Product - Replacement Request

    Hello Customer Support Team,

    My order ORD-45821 arrived today, but the product
    was damaged when I received it.

    I would like to request a replacement.

    Please let me know the next steps.

    Regards,
    Angappan
    """

    support_analysis = """
    Intent: Replacement request

    Category: Damaged product / Order issue

    Customer: Angappan

    Customer Email: angappanmuthusamy@gmail.com

    Order Number: ORD-45821

    Problem:
    The customer reports that the product arrived damaged.

    Priority: High

    Recommended Action:
    Verify the order and initiate the appropriate replacement process.
    """

    print("Creating Response Generator Agent...")

    agent = create_response_generator_agent()

    task = create_response_generator_task(agent)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    print()
    print("Generating customer response...")
    print("=" * 70)

    result = crew.kickoff(
        inputs={
            "customer_email": customer_email,
            "support_analysis": support_analysis,
        }
    )

    print()
    print("=" * 70)
    print("CUSTOMER RESPONSE DRAFT")
    print("=" * 70)
    print(result)
    print("=" * 70)


if __name__ == "__main__":
    main()

    