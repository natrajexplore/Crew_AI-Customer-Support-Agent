from crewai import LLM
from config.settings import OPENAI_MODEL

def main():

    print("Initializing CrewAI LLM...")

    llm = LLM(
        model=f"openai/{OPENAI_MODEL}",
        temperature=0.2,
    )

    print("Sending test request...")
    print()

    response = llm.call(
        "You are a customer support assistant. "
        "Write one short professional greeting to a customer."
    )

    print("LLM Response:")
    print("-" * 60)
    print(response)
    print("-" * 60)


if __name__ == "__main__":
    main()


