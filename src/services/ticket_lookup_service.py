# ---------------------------------------------------------
# TICKET LOOKUP SERVICE
# ---------------------------------------------------------

def get_processed_message_ids(
    service,
    spreadsheet_id,
):
    """
    Retrieve all Gmail Message IDs that already
    exist in the Tickets sheet.

    Gmail Message ID is stored in Column B.
    """

    response = (
        service
        .spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="Tickets!B:B",
        )
        .execute()
    )

    rows = response.get(
        "values",
        []
    )

    processed_ids = set()

    # Skip header
    for row in rows[1:]:

        if not row:
            continue

        message_id = row[0].strip()

        if message_id:
            processed_ids.add(
                message_id
            )

    return processed_ids


def is_message_already_processed(
    service,
    spreadsheet_id,
    message_id,
):
    """
    Check whether a Gmail message has already
    been processed and stored as a ticket.
    """

    processed_ids = (
        get_processed_message_ids(
            service,
            spreadsheet_id,
        )
    )

    return message_id in processed_ids

