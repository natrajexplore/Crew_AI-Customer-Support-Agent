from customer_support_pipeline import clean_customer_response


def test_customer_response_signature():
    response = """
    Dear Angappan,

    Your order arrived damaged.

    Best regards,

    [Your Name]
    Customer Support Team
    """

    result = clean_customer_response(response)

    assert "[Maddy]" in result
    assert "Explore Customer Support Team" in result
    assert "[Explore-AI]" in result
    assert "[9999900000]" in result


def test_customer_response_has_single_signature():
    response = """
    Dear Angappan,

    Your order arrived damaged.

    Best regards,

    [Maddy]
    Explore Customer Support Team
    [Explore-AI]
    [9999900000]
    """

    result = clean_customer_response(response)

    assert result.count("[Maddy]") == 1
    assert result.count("Explore Customer Support Team") == 1
    assert result.count("[Explore-AI]") == 1
    assert result.count("[9999900000]") == 1

    