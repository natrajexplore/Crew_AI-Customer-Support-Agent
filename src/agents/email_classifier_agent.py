from crewai import Agent, LLM

from config.settings import OPENAI_MODEL


def create_email_classifier_agent():

    llm = LLM(
        model=f"openai/{OPENAI_MODEL}",
        temperature=0.0,
    )

    agent = Agent(
        role="Customer Support Email Classifier",
        goal=(
            "Determine whether an incoming email is a genuine "
            "customer support request or a non-support email."
        ),
        backstory=(
            "You are the first-line email triage specialist for a "
            "customer support automation system. Your responsibility "
            "is only to classify incoming emails. You must distinguish "
            "genuine customer issues, questions, requests, complaints, "
            "refund requests, order issues, account issues, and other "
            "support-related communications from newsletters, marketing "
            "emails, social-network notifications, advertisements, "
            "system notifications, personal messages, and unrelated "
            "communications."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return agent

