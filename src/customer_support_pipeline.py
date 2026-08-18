import os
import re

from crewai import Crew, Process
from dotenv import load_dotenv

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

from services.google_sheets_service import (
    create_support_ticket,
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# OFFICIAL CUSTOMER SUPPORT SIGNATURE
# =========================================================

EMAIL_SIGNATURE = """Best regards,

[Maddy]
Explore Customer Support Team
[Explore-AI]
[9999900000]"""


# =========================================================
# STEP 1 - EMAIL CLASSIFICATION
# =========================================================

def run_classifier(customer_email):
    """
    Classify the incoming customer email.
    """

    print()
    print("=" * 70)
    print("STEP 1: EMAIL CLASSIFICATION")
    print("=" * 70)

    classifier_agent = create_email_classifier_agent()

    classifier_task = create_email_classifier_task(
        classifier_agent
    )

    crew = Crew(
        agents=[classifier_agent],
        tasks=[classifier_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "customer_email": customer_email
        }
    )

    classification = str(result).strip()

    print()
    print("CLASSIFIER RESULT")
    print("-" * 70)
    print(classification)
    print("-" * 70)

    return classification


# =========================================================
# CHECK CLASSIFICATION
# =========================================================

def is_customer_support(classification):
    """
    Determine whether the classifier identified
    the email as a customer-support request.
    """

    if not classification:
        return False

    return (
        "IS_CUSTOMER_SUPPORT: YES"
        in classification.upper()
    )


# =========================================================
# STEP 2 - CUSTOMER SUPPORT ANALYSIS
# =========================================================

def run_customer_support_agent(customer_email):
    """
    Analyze the customer issue using the
    customer-support CrewAI agent.
    """

    print()
    print("=" * 70)
    print("STEP 2: CUSTOMER SUPPORT ANALYSIS")
    print("=" * 70)

    support_agent = create_customer_support_agent()

    support_task = create_customer_analysis_task(
        support_agent
    )

    crew = Crew(
        agents=[support_agent],
        tasks=[support_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "customer_email": customer_email
        }
    )

    support_analysis = str(
        result
    ).strip()

    print()
    print("CUSTOMER SUPPORT ANALYSIS")
    print("-" * 70)
    print(support_analysis)
    print("-" * 70)

    return support_analysis


# =========================================================
# STEP 3 - RESPONSE GENERATION
# =========================================================

def run_response_generator(
    customer_email,
    support_analysis,
):
    """
    Generate the customer-facing response.
    """

    print()
    print("=" * 70)
    print("STEP 3: RESPONSE GENERATION")
    print("=" * 70)

    response_agent = (
        create_response_generator_agent()
    )

    response_task = (
        create_response_generator_task(
            response_agent
        )
    )

    crew = Crew(
        agents=[response_agent],
        tasks=[response_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "customer_email": customer_email,
            "support_analysis": str(
                support_analysis
            ),
        }
    )

    response = str(
        result
    ).strip()

    print()
    print("GENERATED CUSTOMER RESPONSE")
    print("-" * 70)
    print(response)
    print("-" * 70)

    return response


# =========================================================
# CLEAN AI RESPONSE
# =========================================================

def clean_customer_response(
    draft_response
):
    """
    Clean the AI-generated response before it
    is saved to Google Sheets.

    The AI response may accidentally contain:
        - Subject:
        - Best regards
        - Kind regards
        - Regards
        - AI-generated signatures
        - [Your Name]
        - [Your Company]
        - [Your Contact Information]
        - Our official signature

    This function removes those elements and
    adds exactly ONE official signature.
    """

    if draft_response is None:
        response = ""
    else:
        response = str(
            draft_response
        ).strip()

    # -----------------------------------------------------
    # Remove accidental markdown code fences
    # -----------------------------------------------------

    response = re.sub(
        r"^```(?:text|plain|email)?\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"\s*```$",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = response.strip()

    # -----------------------------------------------------
    # Remove Subject line
    # -----------------------------------------------------

    lines = response.splitlines()

    cleaned_lines = []

    for line in lines:

        stripped = line.strip()

        if stripped.lower().startswith(
            "subject:"
        ):
            continue

        cleaned_lines.append(line)

    response = "\n".join(
        cleaned_lines
    ).strip()

    # -----------------------------------------------------
    # Remove AI-generated signature block
    # -----------------------------------------------------

    lines = response.splitlines()

    signature_markers = [
        "[Your Name]",
        "[Your Company]",
        "[Your Contact Information]",
        "[Your Contact Info]",
        "[Maddy]",
        "[Explore-AI]",
        "[9999900000]",
    ]

    signature_start = None

    for index, line in enumerate(
        lines
    ):

        stripped = line.strip()

        if not stripped:
            continue

        for marker in signature_markers:

            if marker.lower() in (
                stripped.lower()
            ):
                signature_start = index
                break

        if signature_start is not None:
            break

    if signature_start is not None:

        response = "\n".join(
            lines[
                :signature_start
            ]
        ).strip()

    # -----------------------------------------------------
    # Remove common AI signature phrases
    # -----------------------------------------------------

    lines = response.splitlines()

    cleaned_lines = []

    for line in lines:

        stripped_lower = (
            line.strip().lower()
        )

        if stripped_lower in [
            "customer support team",
            "explore customer support team",
            "[your name]",
            "[your company]",
            "[your contact information]",
            "[your contact info]",
        ]:
            continue

        cleaned_lines.append(line)

    response = "\n".join(
        cleaned_lines
    ).strip()

    # -----------------------------------------------------
    # Remove trailing closing phrases
    #
    # This is important because the AI may generate:
    #
    # Best regards,
    #
    # and then the application adds another:
    #
    # Best regards,
    #
    # -----------------------------------------------------

    lines = response.splitlines()

    while lines:

        last_line = lines[-1].strip().lower()

        if last_line in [
            "best regards",
            "best regards,",
            "kind regards",
            "kind regards,",
            "warm regards",
            "warm regards,",
            "regards",
            "regards,",
            "sincerely",
            "sincerely,",
            "yours sincerely",
            "yours sincerely,",
        ]:
            lines.pop()
            continue

        if last_line == "":
            lines.pop()
            continue

        break

    response = "\n".join(
        lines
    ).strip()

    # -----------------------------------------------------
    # Remove accidental duplicate official signature
    # -----------------------------------------------------

    official_marker = "[Maddy]"

    if official_marker.lower() in (
        response.lower()
    ):

        index = response.lower().find(
            official_marker.lower()
        )

        response = response[
            :index
        ].strip()

    # -----------------------------------------------------
    # Remove duplicate Explore-AI signature
    # -----------------------------------------------------

    for marker in [
        "[Explore-AI]",
        "[9999900000]",
    ]:

        if marker.lower() in (
            response.lower()
        ):

            index = response.lower().find(
                marker.lower()
            )

            response = response[
                :index
            ].strip()

    # -----------------------------------------------------
    # Final safety cleanup
    # -----------------------------------------------------

    response = response.strip()

    # -----------------------------------------------------
    # Add EXACTLY ONE official signature
    # -----------------------------------------------------

    final_response = (
        response
        + "\n\n"
        + EMAIL_SIGNATURE
    )

    return final_response.strip()


# =========================================================
# STEP 4 - SAVE TO GOOGLE SHEETS
# =========================================================

def save_to_google_sheets(
    customer_email,
    classification,
    support_analysis,
    draft_response,
):
    """
    Save the generated customer-support ticket
    into Google Sheets with PENDING_REVIEW status.
    """

    print()
    print("=" * 70)
    print("STEP 4: SAVING SUPPORT TICKET")
    print("=" * 70)

    spreadsheet_id = os.getenv(
        "GOOGLE_SHEET_ID"
    )

    if not spreadsheet_id:

        raise ValueError(
            "GOOGLE_SHEET_ID is not configured "
            "in the .env file."
        )

    ticket_result = create_support_ticket(
        spreadsheet_id=spreadsheet_id,
        customer_email=customer_email,
        support_analysis=support_analysis,
        draft_reply=draft_response,
        classification=classification,
    )

    print()
    print("SUPPORT TICKET CREATED")
    print("-" * 70)

    print(
        f"Ticket ID : "
        f"{ticket_result['ticket_id']}"
    )

    print(
        f"Status    : "
        f"{ticket_result['status']}"
    )

    print(
        f"Sheet     : "
        f"{ticket_result['updated_range']}"
    )

    print("-" * 70)

    return ticket_result


# =========================================================
# COMPLETE CUSTOMER SUPPORT PIPELINE
# =========================================================

def run_customer_support_pipeline(
    customer_email
):
    """
    Complete customer-support AI workflow:

        1. Classify email
        2. Check customer-support category
        3. Analyze issue
        4. Generate response
        5. Clean response
        6. Add official signature
        7. Save ticket to Google Sheets
        8. Wait for human approval

    No email is sent from this function.
    """

    print()
    print("=" * 70)
    print("CUSTOMER SUPPORT AI PIPELINE")
    print("=" * 70)

    # =====================================================
    # STEP 1 - CLASSIFICATION
    # =====================================================

    classification = run_classifier(
        customer_email
    )

    # =====================================================
    # FILTER NON-SUPPORT EMAIL
    # =====================================================

    if not is_customer_support(
        classification
    ):

        print()
        print("=" * 70)
        print("EMAIL IS NOT CUSTOMER SUPPORT")
        print("=" * 70)

        print(
            "No customer-support workflow "
            "will be executed."
        )

        return {
            "status": "IGNORED",
            "classification": classification,
        }

    # =====================================================
    # STEP 2 - CUSTOMER SUPPORT ANALYSIS
    # =====================================================

    support_analysis = (
        run_customer_support_agent(
            customer_email
        )
    )

    # =====================================================
    # STEP 3 - RESPONSE GENERATION
    # =====================================================

    draft_response = (
        run_response_generator(
            customer_email,
            support_analysis,
        )
    )

    # =====================================================
    # CLEAN RESPONSE
    # =====================================================

    draft_response = (
        clean_customer_response(
            draft_response
        )
    )

    # =====================================================
    # SHOW FINAL CUSTOMER RESPONSE
    # =====================================================

    print()
    print("=" * 70)
    print("FINAL CUSTOMER RESPONSE")
    print("=" * 70)
    print()
    print(draft_response)
    print()
    print("=" * 70)

    # =====================================================
    # STEP 4 - SAVE TICKET
    # =====================================================

    ticket_result = (
        save_to_google_sheets(
            customer_email=customer_email,
            classification=classification,
            support_analysis=support_analysis,
            draft_response=draft_response,
        )
    )

    # =====================================================
    # FINAL STATUS
    # =====================================================

    print()
    print("=" * 70)
    print("CUSTOMER SUPPORT PIPELINE COMPLETED")
    print("=" * 70)

    print(
        f"Ticket ID : "
        f"{ticket_result['ticket_id']}"
    )

    print(
        "Status    : PENDING_REVIEW"
    )

    print(
        "Approval  : PENDING"
    )

    print(
        "Email     : NOT SENT"
    )

    print(
        "Human approval is required before sending."
    )

    print("=" * 70)

    return {
        "status": "PENDING_REVIEW",
        "classification": classification,
        "support_analysis": str(
            support_analysis
        ),
        "draft_response": str(
            draft_response
        ),
        "ticket": ticket_result,
    }
