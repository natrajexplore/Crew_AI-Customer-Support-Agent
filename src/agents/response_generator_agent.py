from crewai import Agent, LLM
from config.settings import OPENAI_MODEL

def create_response_generator_agent():

    llm = LLM(
        model=f"openai/{OPENAI_MODEL}",
        temperature=0.2,
    )

    agent = Agent(
        role="Customer Support Response Writer",
        goal=(
            "Create accurate, professional, concise, and empathetic "
            "customer support email responses based only on the "
            "customer email and support analysis provided."
        ),
        backstory=(
            "You are an experienced customer support communication "
            "specialist. You write clear business emails that address "
            "the customer's actual concern without inventing policies, "
            "refund amounts, delivery dates, guarantees, or other "
            "information that has not been provided."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    return agent

