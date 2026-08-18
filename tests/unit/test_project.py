def test_python_environment():
    import sys

    assert sys.version_info >= (3, 11)


def test_google_sheets_service_import():
    from services.google_sheets_service import (
        get_google_sheets_service,
    )

    assert callable(get_google_sheets_service)


def test_gmail_service_import():
    from services.gmail_service import (
        get_gmail_service,
    )

    assert callable(get_gmail_service)


def test_gmail_sender_import():
    from services.gmail_sender_service import (
        get_gmail_sender_service,
    )

    assert callable(get_gmail_sender_service)


def test_customer_support_agents_import():
    from agents.email_classifier_agent import (
        create_email_classifier_agent,
    )

    from agents.customer_support_agent import (
        create_customer_support_agent,
    )

    from agents.response_generator_agent import (
        create_response_generator_agent,
    )

    assert callable(create_email_classifier_agent)
    assert callable(create_customer_support_agent)
    assert callable(create_response_generator_agent)


def test_ticket_processor_import():
    from services.ticket_processor import (
        process_approved_tickets,
    )

    assert callable(process_approved_tickets)

    