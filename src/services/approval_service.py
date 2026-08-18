def get_approved_tickets(
    service,
    spreadsheet_id,
):
    """
    Read the Tickets sheet and return tickets
    where Column P (Approval) is APPROVED.

    Sheet structure:

    A = Ticket ID
    B = Gmail Message ID
    C = Gmail Thread ID
    D = Customer Name
    E = Customer Email
    F = Subject
    G = Category
    H = Priority
    I = Customer Issue
    J = Support Analysis
    K = Draft Reply
    L = Status
    M = Created At
    N = Reviewed By
    O = Review Notes
    P = Approval
    Q = Approval Timestamp
    R = Final Response
    """

    response = (
        service
        .spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="Tickets!A:R",
        )
        .execute()
    )

    rows = response.get(
        "values",
        []
    )

    if len(rows) <= 1:
        return []

    approved_tickets = []

    # Skip header row
    for row_number, row in enumerate(
        rows[1:],
        start=2,
    ):

        # Make sure every row has 18 columns
        row = row + [""] * (
            18 - len(row)
        )

        ticket_id = row[0]
        gmail_message_id = row[1]
        gmail_thread_id = row[2]
        customer_name = row[3]
        customer_email = row[4]
        subject = row[5]
        category = row[6]
        priority = row[7]
        customer_issue = row[8]
        support_analysis = row[9]
        draft_reply = row[10]

        status = row[11].strip().upper()

        created_at = row[12]
        reviewed_by = row[13]
        review_notes = row[14]

        # Column P = index 15
        approval = row[15].strip().upper()

        approval_timestamp = row[16]
        final_response = row[17]

        print()
        print(
            f"Checking row {row_number}: "
            f"{ticket_id}"
        )

        print(
            f"  Status   : {status}"
        )

        print(
            f"  Approval : {approval}"
        )

        # Only approved and unsent tickets
        if (
            approval == "APPROVED"
            and status != "SENT"
        ):

            ticket = {
                "Ticket ID": ticket_id,
                "Gmail Message ID": gmail_message_id,
                "Gmail Thread ID": gmail_thread_id,
                "Customer Name": customer_name,
                "Customer Email": customer_email,
                "Subject": subject,
                "Category": category,
                "Priority": priority,
                "Customer Issue": customer_issue,
                "Support Analysis": support_analysis,
                "Draft Reply": draft_reply,
                "Status": status,
                "Created At": created_at,
                "Reviewed By": reviewed_by,
                "Review Notes": review_notes,
                "Approval": approval,
                "Approval Timestamp": approval_timestamp,
                "Final Response": final_response,
                "_row_number": row_number,
            }

            approved_tickets.append(
                ticket
            )

    return approved_tickets


def update_ticket_status(
    service,
    spreadsheet_id,
    row_number,
    status,
    approval_timestamp="",
    final_response="",
):
    """
    Update only the fields that change
    during approval processing.
    """

    # -----------------------------------------------------
    # Update Status - Column L
    # -----------------------------------------------------

    (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"Tickets!L{row_number}",
            valueInputOption="USER_ENTERED",
            body={
                "values": [[status]]
            },
        )
        .execute()
    )

    # -----------------------------------------------------
    # Update Approval Timestamp - Column Q
    # -----------------------------------------------------

    (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"Tickets!Q{row_number}",
            valueInputOption="USER_ENTERED",
            body={
                "values": [[
                    approval_timestamp
                ]]
            },
        )
        .execute()
    )

    # -----------------------------------------------------
    # Update Final Response - Column R
    # -----------------------------------------------------

    (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"Tickets!R{row_number}",
            valueInputOption="USER_ENTERED",
            body={
                "values": [[
                    final_response
                ]]
            },
        )
        .execute()
    )

def get_rejected_tickets(
    service,
    spreadsheet_id,
):
    """
    Find tickets that have been rejected
    by the human reviewer.
    """

    response = (
        service
        .spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range="Tickets!A:R",
        )
        .execute()
    )

    rows = response.get(
        "values",
        []
    )

    rejected_tickets = []

    if not rows:
        return rejected_tickets

    headers = rows[0]

    for row_number, row in enumerate(
        rows[1:],
        start=2,
    ):

        # Make row same length as headers
        row = row + [
            ""
        ] * (
            len(headers) - len(row)
        )

        ticket = dict(
            zip(
                headers,
                row
            )
        )

        ticket[
            "_row_number"
        ] = row_number

        status = ticket.get(
            "Status",
            ""
        ).strip().upper()

        approval = ticket.get(
            "Approval",
            ""
        ).strip().upper()

        if (
            approval == "REJECTED"
            and status
            not in [
                "CLOSED",
                "SENT",
            ]
        ):

            rejected_tickets.append(
                ticket
            )

    return rejected_tickets

def mark_ticket_rejected(
    service,
    spreadsheet_id,
    row_number,
    review_notes="",
):
    """
    Mark a rejected ticket as CLOSED.
    """

    from datetime import datetime

    timestamp = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    values = [
        [
            "CLOSED",        # Status
            timestamp,       # Approval Timestamp
            review_notes,    # Review Notes
        ]
    ]

    response = (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=(
                f"Tickets!O{row_number}:Q"
                f"{row_number}"
            ),
            valueInputOption="USER_ENTERED",
            body={
                "values": [
                    [
                        review_notes,
                        timestamp,
                        "CLOSED",
                    ]
                ]
            },
        )
        .execute()
    )

    return response

    def mark_ticket_rejected(
    service,
    spreadsheet_id,
    row_number,
    review_notes="",
):
        """
        Mark a rejected ticket as CLOSED.
        """

    from datetime import datetime

    timestamp = (
        datetime.now().isoformat(
            timespec="seconds"
        )
    )

    # -----------------------------------------------------
    # Update Status
    # -----------------------------------------------------

    (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"Tickets!L{row_number}",
            valueInputOption="USER_ENTERED",
            body={
                "values": [
                    ["CLOSED"]
                ]
            },
        )
        .execute()
    )

    # -----------------------------------------------------
    # Update Review Notes
    # -----------------------------------------------------

    (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"Tickets!O{row_number}",
            valueInputOption="USER_ENTERED",
            body={
                "values": [
                    [review_notes]
                ]
            },
        )
        .execute()
    )

    # -----------------------------------------------------
    # Update Approval Timestamp
    # -----------------------------------------------------

    response = (
        service
        .spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"Tickets!Q{row_number}",
            valueInputOption="USER_ENTERED",
            body={
                "values": [
                    [timestamp]
                ]
            },
        )
        .execute()
    )

    return response
