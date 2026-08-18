from crewai import Agent, LLM
from config.settings import OPENAI_MODEL


def create_customer_support_agent():

    llm = LLM(
        model=f"openai/{OPENAI_MODEL}",
        temperature=0.2,
    )

    agent = Agent(
        role="Customer Support Analyst",
        goal=(
            "Analyze incoming customer support emails accurately, "
            "identify the customer's intent and issue, determine "
            "priority, extract important information, and recommend "
            "the appropriate next action."
        ),
        backstory=(
            "You are an experienced customer support analyst working "
            "for a professional customer service organization. "
            "You carefully read customer emails, identify the real "
            "problem, distinguish facts from assumptions, and produce "
            "clear structured analysis for downstream support agents. "
            "You never invent customer information."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return agent
