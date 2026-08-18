from crewai import Crew, Process
from agents.customer_support_agent import (
    create_customer_support_agent,
)
from agents.customer_support_task import (
    create_customer_analysis_task,
)


def main():

    customer_email = """
    From: angappanmuthusamt@mgail.com
    Subject: Damaged product received

    Hello Support Team,

    I received my order #ORD-45821 today, but unfortunately
    the product arrived damaged.

    I would like to get a replacement as soon as possible.

    Please let me know what I need to do next.

    Thanks,
    Angappan
    """

    print("Creating Customer Support Agent...")

    agent = create_customer_support_agent()

    task = create_customer_analysis_task(agent)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    print()
    print("Starting customer email analysis...")
    print("=" * 70)

    result = crew.kickoff(
        inputs={
            "customer_email": customer_email
        }
    )

    print()
    print("=" * 70)
    print("CUSTOMER SUPPORT ANALYSIS")
    print("=" * 70)
    print(result)
    print("=" * 70)


if __name__ == "__main__":
    main()

