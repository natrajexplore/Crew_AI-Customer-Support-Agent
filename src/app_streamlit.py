import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from services.google_sheets_service import get_google_sheets_service
from services.ticket_processor import process_approved_tickets


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")

SHEET_RANGE = "Tickets!A:R"

EXPECTED_HEADERS = [
    "Ticket ID",
    "Gmail Message ID",
    "Gmail Thread ID",
    "Customer Name",
    "Customer Email",
    "Subject",
    "Category",
    "Priority",
    "Customer Issue",
    "Support Analysis",
    "Draft Reply",
    "Status",
    "Created At",
    "Reviewed By",
    "Review Notes",
    "Approval",
    "Approval Timestamp",
    "Final Response",
]

st.set_page_config(
    page_title="Explore-AI Support Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PREMIUM UI STYLING
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background: #111827;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 24px 28px;
        border-radius: 18px;
        background: linear-gradient(135deg, #111827, #312e81);
        color: white;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px rgba(17,24,39,.18);
    }

    .hero h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 750;
    }

    .hero p {
        margin: 8px 0 0 0;
        opacity: .82;
        font-size: 15px;
    }

    .status-pill {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,.13);
        font-size: 13px;
        margin-top: 14px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #111827;
        margin: 12px 0 14px 0;
    }

    .ticket-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px;
        margin: 12px 0 20px 0;
        box-shadow: 0 5px 20px rgba(15,23,42,.07);
    }

    .ticket-title {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
    }

    .ticket-subtitle {
        color: #6b7280;
        font-size: 14px;
        margin-top: 4px;
    }

    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: #eef2ff;
        color: #3730a3;
        font-size: 12px;
        font-weight: 700;
        margin-right: 6px;
    }

    .priority-high {
        background: #fee2e2;
        color: #991b1b;
    }

    .priority-medium {
        background: #fef3c7;
        color: #92400e;
    }

    .priority-low {
        background: #dcfce7;
        color: #166534;
    }

    .metric-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 4px 16px rgba(15,23,42,.05);
    }

    .metric-label {
        color: #6b7280;
        font-size: 13px;
    }

    .metric-value {
        color: #111827;
        font-size: 28px;
        font-weight: 750;
        margin-top: 5px;
    }

    .pipeline {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(15,23,42,.05);
    }

    .pipeline-step {
        text-align: center;
        font-size: 13px;
        color: #374151;
    }

    .pipeline-icon {
        font-size: 28px;
        margin-bottom: 5px;
    }

    .activity {
        background: white;
        border-left: 4px solid #4f46e5;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 8px;
        color: #374151;
    }

    .footer {
        text-align: center;
        color: #9ca3af;
        padding: 28px 0 10px 0;
        font-size: 12px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 650;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "pipeline_output" not in st.session_state:
    st.session_state.pipeline_output = ""

if "last_action" not in st.session_state:
    st.session_state.last_action = ""


# =========================================================
# CONNECTION
# =========================================================

@st.cache_resource
def get_sheets_service():
    return get_google_sheets_service()


def get_sheet_data():
    service = get_sheets_service()

    response = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_RANGE,
        )
        .execute()
    )

    values = response.get("values", [])

    if not values:
        return pd.DataFrame(columns=EXPECTED_HEADERS)

    rows = []

    for row in values[1:]:
        row = row + [""] * (len(EXPECTED_HEADERS) - len(row))
        row = row[:len(EXPECTED_HEADERS)]
        rows.append(row)

    return pd.DataFrame(rows, columns=EXPECTED_HEADERS)


def update_cell(row_number, column, value):
    service = get_sheets_service()

    (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Tickets!{column}{row_number}",
            valueInputOption="USER_ENTERED",
            body={"values": [[value]]},
        )
        .execute()
    )


def update_ticket(
    row_number,
    draft_reply=None,
    approval=None,
    status=None,
    review_notes=None,
    reviewed_by=None,
    final_response=None,
):
    if draft_reply is not None:
        update_cell(row_number, "K", draft_reply)

    if status is not None:
        update_cell(row_number, "L", status)

    if reviewed_by is not None:
        update_cell(row_number, "N", reviewed_by)

    if review_notes is not None:
        update_cell(row_number, "O", review_notes)

    if approval is not None:
        update_cell(row_number, "P", approval)

    if approval is not None:
        update_cell(
            row_number,
            "Q",
            datetime.now().isoformat(timespec="seconds"),
        )

    if final_response is not None:
        update_cell(row_number, "R", final_response)


def run_crewai_pipeline():
    app_file = BASE_DIR / "crewai-app.py"

    result = subprocess.run(
        [sys.executable, str(app_file)],
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
    )

    return result.returncode, result.stdout + "\n" + result.stderr


def priority_class(priority):
    value = str(priority).lower()

    if "high" in value:
        return "priority-high"

    if "medium" in value:
        return "priority-medium"

    return "priority-low"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 🤖 Explore-AI")
    st.caption("Customer Support Operations Center")

    st.divider()

    st.markdown("### Navigation")
    st.markdown("🏠 Command Center")
    st.markdown("📥 Customer Inbox")
    st.markdown("👤 Human Approval")
    st.markdown("📤 Sent Tickets")
    st.markdown("📊 Analytics")

    st.divider()

    st.markdown("### System")
    st.success("Gmail Connected")
    st.success("Google Sheets Connected")
    st.success("CrewAI Ready")

    st.divider()

    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()


# =========================================================
# VALIDATION
# =========================================================

if not SPREADSHEET_ID:
    st.error("GOOGLE_SHEET_ID is missing from your .env file.")
    st.stop()


try:
    df = get_sheet_data()
except Exception as error:
    st.error(f"Unable to read Google Sheets: {error}")
    st.stop()


for column in ["Status", "Approval", "Priority"]:
    if column in df.columns:
        df[column] = df[column].fillna("").astype(str).str.strip().str.upper()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>Explore-AI Customer Support</h1>
        <p>Intelligent Customer Support Operations Center</p>
        <div class="status-pill">● AI SYSTEM ONLINE · HUMAN-IN-THE-LOOP ENABLED</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# METRICS
# =========================================================

total = len(df)

pending = len(
    df[df["Status"] == "PENDING_REVIEW"]
)

approved_waiting = len(
    df[
        (df["Approval"] == "APPROVED")
        & (df["Status"] != "SENT")
    ]
)

sent = len(
    df[df["Status"] == "SENT"]
)

rejected = len(
    df[df["Approval"] == "REJECTED"]
)

ignored = len(
    df[df["Status"] == "IGNORED"]
)

metrics = [
    ("📩", "Total Tickets", total),
    ("⏳", "Pending Review", pending),
    ("✅", "Approved", approved_waiting),
    ("📤", "Sent", sent),
    ("❌", "Rejected", rejected),
    ("🚫", "Ignored", ignored),
]

cols = st.columns(6)

for col, (icon, label, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{icon} {label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# PIPELINE
# =========================================================

st.markdown(
    '<div class="section-title">⚡ AI Support Pipeline</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="pipeline">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div class="pipeline-step">
                <div class="pipeline-icon">📧</div>
                <b>Gmail</b><br>Receive
            </div>
            <div>→</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">🧠</div>
                <b>Classifier</b><br>Understand
            </div>
            <div>→</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">🔍</div>
                <b>AI Analyst</b><br>Analyze
            </div>
            <div>→</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">✍️</div>
                <b>Response AI</b><br>Draft
            </div>
            <div>→</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">👤</div>
                <b>Human</b><br>Approve
            </div>
            <div>→</div>
            <div class="pipeline-step">
                <div class="pipeline-icon">📤</div>
                <b>Gmail</b><br>Send
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# RUN AI PIPELINE
# =========================================================

left, right = st.columns([3, 1])

with left:
    st.markdown(
        '<div class="section-title">📥 Process New Customer Emails</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Run the existing CrewAI workflow. New support emails become "
        "PENDING_REVIEW tickets; no email is automatically sent."
    )

with right:
    if st.button(
        "🚀 Run AI Agent",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Running CrewAI pipeline..."):
            return_code, output = run_crewai_pipeline()

        st.session_state.pipeline_output = output

        if return_code == 0:
            st.success("AI pipeline completed.")
        else:
            st.error("AI pipeline returned an error.")


if st.session_state.pipeline_output:
    with st.expander("🔎 View AI Pipeline Execution Log"):
        st.code(st.session_state.pipeline_output, language="text")


# =========================================================
# HUMAN APPROVAL
# =========================================================

st.markdown(
    '<div class="section-title">👤 Human Approval Center</div>',
    unsafe_allow_html=True,
)

approval_df = df[
    (df["Status"] == "PENDING_REVIEW")
    & (df["Approval"] != "APPROVED")
    & (df["Approval"] != "REJECTED")
]

if approval_df.empty:
    st.success("🎉 No responses currently require human approval.")
else:
    st.warning(
        f"⚠️ {len(approval_df)} response(s) require human review before sending."
    )

    for index, row in approval_df.iterrows():
        sheet_row = index + 2

        ticket_id = row["Ticket ID"]
        customer = row["Customer Name"] or "Customer"
        email = row["Customer Email"]
        subject = row["Subject"]
        category = row["Category"]
        priority = row["Priority"]
        issue = row["Customer Issue"]
        analysis = row["Support Analysis"]
        draft = row["Draft Reply"]

        st.markdown(
            '<div class="ticket-card">',
            unsafe_allow_html=True,
        )

        title_col, badge_col = st.columns([5, 1])

        with title_col:
            st.markdown(
                f'<div class="ticket-title">🎫 {ticket_id}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="ticket-subtitle">{subject}</div>',
                unsafe_allow_html=True,
            )

        with badge_col:
            st.markdown(
                f'<span class="badge {priority_class(priority)}">{priority or "NORMAL"}</span>',
                unsafe_allow_html=True,
            )

        info1, info2, info3 = st.columns(3)

        with info1:
            st.markdown(f"**👤 Customer**  \n{customer}")

        with info2:
            st.markdown(f"**✉ Email**  \n{email}")

        with info3:
            st.markdown(f"**📂 Category**  \n{category}")

        st.markdown("---")

        st.markdown("**📦 Customer Issue**")
        st.info(issue or "Issue details not provided.")

        with st.expander("🧠 AI Support Analysis", expanded=True):
            st.write(analysis)

        st.markdown("**✍️ AI Generated Response**")

        edited_response = st.text_area(
            "Review and edit before approval",
            value=draft,
            height=260,
            key=f"draft_editor_{sheet_row}",
            label_visibility="collapsed",
        )

        review_notes = st.text_input(
            "Review notes (optional)",
            key=f"review_notes_{sheet_row}",
        )

        st.markdown("---")

        edit_col, reject_col, approve_col = st.columns(3)

        with edit_col:
            if st.button(
                "💾 Save Draft",
                key=f"save_{sheet_row}",
                use_container_width=True,
            ):
                update_ticket(
                    row_number=sheet_row,
                    draft_reply=edited_response,
                    review_notes=review_notes,
                )
                st.success("Draft saved.")
                st.rerun()

        with reject_col:
            if st.button(
                "❌ Reject",
                key=f"reject_{sheet_row}",
                use_container_width=True,
            ):
                update_ticket(
                    row_number=sheet_row,
                    draft_reply=edited_response,
                    approval="REJECTED",
                    status="CLOSED",
                    review_notes=review_notes or "Rejected by reviewer.",
                    reviewed_by="Streamlit Reviewer",
                )
                st.error(f"{ticket_id} rejected.")
                st.rerun()

        with approve_col:
            if st.button(
                "✅ Approve",
                key=f"approve_{sheet_row}",
                type="primary",
                use_container_width=True,
            ):
                update_ticket(
                    row_number=sheet_row,
                    draft_reply=edited_response,
                    approval="APPROVED",
                    status="PENDING_REVIEW",
                    review_notes=review_notes,
                    reviewed_by="Streamlit Reviewer",
                )
                st.success(
                    f"{ticket_id} approved. It is now waiting in the send queue."
                )
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# APPROVED SEND QUEUE
# =========================================================

st.markdown(
    '<div class="section-title">📤 Approved Send Queue</div>',
    unsafe_allow_html=True,
)

send_df = df[
    (df["Approval"] == "APPROVED")
    & (df["Status"] != "SENT")
]

if send_df.empty:
    st.info("No approved tickets are waiting to be sent.")
else:
    st.warning(
        f"{len(send_df)} approved ticket(s) are ready for Gmail delivery."
    )

    st.dataframe(
        send_df[
            [
                "Ticket ID",
                "Customer Name",
                "Customer Email",
                "Subject",
                "Status",
                "Approval",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        "**Safety checkpoint:** Approval is recorded first. "
        "Sending is a separate action."
    )

    if st.button(
        "🚀 Send Approved Responses",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Sending approved responses through Gmail..."):
            try:
                process_approved_tickets()
                st.success(
                    "Approved responses processed successfully."
                )
                st.rerun()
            except Exception as error:
                st.error(
                    f"Unable to send approved responses: {error}"
                )


# =========================================================
# RECENTLY SENT
# =========================================================

st.markdown(
    '<div class="section-title">📨 Recently Sent Tickets</div>',
    unsafe_allow_html=True,
)

sent_df = df[df["Status"] == "SENT"]

if sent_df.empty:
    st.info("No sent tickets yet.")
else:
    st.dataframe(
        sent_df[
            [
                "Ticket ID",
                "Customer Name",
                "Customer Email",
                "Subject",
                "Category",
                "Status",
                "Approval",
                "Created At",
            ]
        ].tail(10),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# ACTIVITY
# =========================================================

st.markdown(
    '<div class="section-title">🕒 Recent AI Activity</div>',
    unsafe_allow_html=True,
)

recent = df.tail(5)

if recent.empty:
    st.info("No activity available.")
else:
    for _, row in recent.iloc[::-1].iterrows():
        ticket_id = row.get("Ticket ID", "")
        status = row.get("Status", "")
        approval = row.get("Approval", "")

        if status == "SENT":
            event = "📤 Response sent through Gmail"
        elif approval == "APPROVED":
            event = "✅ Human approval recorded"
        elif status == "PENDING_REVIEW":
            event = "👤 Waiting for human approval"
        else:
            event = "🧠 Ticket processed by AI"

        st.markdown(
            f"""
            <div class="activity">
                <b>{ticket_id}</b> · {event}
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Explore-AI Customer Support · CrewAI · Gmail · Google Sheets ·
        Human-in-the-Loop
    </div>
    """,
    unsafe_allow_html=True,
)

