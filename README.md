🤖 Explore-AI Customer Support Agent

🚀 Intelligent Customer Support Automation with CrewAI

Gmail 📧 + CrewAI 🤖 + Google Sheets 📊 + Streamlit 🖥️ + Human-in-the-Loop 👤

🌟 Project Overview

Explore-AI Customer Support Agent is an AI-powered customer support automation platform designed to reduce repetitive support activities while keeping human approval at the center of customer communication.

The system automatically reads customer emails, understands the request using CrewAI agents, analyzes the issue, generates a professional response, creates a support ticket, and waits for a human reviewer before the response is sent.

💡 AI handles the repetitive work. Humans make the final decision.

🎯 What Problem Does It Solve?

Customer-support teams frequently spend valuable time on repetitive activities:

📥 Reading incoming emails
🏷️ Categorizing customer requests
🔍 Understanding customer issues
✍️ Writing repetitive responses
📋 Creating and tracking tickets
📤 Sending approved responses

Explore-AI automates these activities while preserving human control over the final customer communication.

⚡ End-to-End Workflow

                    📧 CUSTOMER EMAIL
                           │
                           ▼
                    ┌─────────────┐
                    │  Gmail API  │
                    └──────┬──────┘
                           │
                           ▼
                 🤖 EMAIL CLASSIFIER
                           │
                    ┌──────┴──────┐
                    │             │
                 SUPPORT       NON-SUPPORT
                    │             │
                    ▼             ▼
          🔍 CUSTOMER ANALYSIS   🚫 IGNORE
                    │
                    ▼
             ✍️ RESPONSE AI
                    │
                    ▼
          🧹 RESPONSE CLEANUP
                    │
                    ▼
             📊 GOOGLE SHEETS
                    │
                    ▼
             ⏳ PENDING_REVIEW
                    │
                    ▼
          🖥️ STREAMLIT DASHBOARD
                    │
             👤 HUMAN REVIEW
                    │
              ┌─────┴─────┐
              │           │
          ✅ APPROVE    ❌ REJECT
              │           │
              ▼           ▼
       📤 SEND QUEUE    🔒 CLOSED
              │
              ▼
          📧 GMAIL API
              │
              ▼
          ✅ SENT

🤖 CrewAI Multi-Agent Architecture

The application uses three specialized AI agents.

1️⃣ 📧 Email Classifier Agent

Purpose: Understand whether an incoming email is a genuine customer-support request.

Responsibilities

📌 Identify support-related emails

🏷️ Determine request category

🎯 Provide classification confidence

🚫 Filter non-support messages

Example:

IS_CUSTOMER_SUPPORT: YES
CATEGORY: Replacement requests
CONFIDENCE: HIGH

2️⃣ 🔍 Customer Support Agent

Purpose: Analyze the customer's actual problem and determine the appropriate support context.

Responsibilities

👤 Identify customer

📦 Extract order information

📝 Understand the reported issue

🏷️ Categorize the request

🚨 Determine priority

💡 Recommend a support action

The agent is designed to avoid inventing unsupported:

Company policies

Refund amounts

Replacement dates

Shipping dates

Guarantees

3️⃣ ✍️ Response Generator Agent

Purpose: Generate a professional customer-facing response.

Response principles

✅ Professional
✅ Concise
✅ Empathetic
✅ Issue-specific
✅ Based on available information
❌ No internal AI analysis
❌ No unsupported claims
❌ No AI-generated signature
❌ No unnecessary subject line

The application adds the official signature separately:

Best regards,

[Maddy]
Explore Customer Support Team
[Explore-AI]
[9999900000]

👤 Human-in-the-Loop Safety

Human approval is a core design principle of this project.

The AI does not automatically send a generated customer response.

          🤖 AI GENERATED RESPONSE
                    │
                    ▼
             ⏳ PENDING_REVIEW
                    │
                    ▼
              👤 HUMAN REVIEW
                    │
             ┌──────┴──────┐
             │             │
             ▼             ▼
         ✅ APPROVE     ❌ REJECT
             │             │
             ▼             ▼
       📤 SEND QUEUE    🔒 CLOSED
             │
             ▼
          📧 GMAIL
             │
             ▼
          ✅ SENT

Reviewer capabilities

👀 Review customer issue
🧠 Review AI analysis
✏️ Edit generated response
📝 Add review notes
✅ Approve
❌ Reject

This provides a controlled and auditable AI-assisted workflow.

🖥️ Premium Streamlit Dashboard

The Streamlit application acts as the Customer Support Operations Center.

Dashboard capabilities

📊 Ticket KPIs
⚡ AI pipeline visualization
📥 Customer-support queue
👤 Human approval center
🧠 AI analysis viewer
✍️ Editable response
❌ Reject workflow
✅ Approve workflow
📤 Approved send queue
📨 Recently sent tickets
🕒 Recent activity
🔌 Service connection indicators

Dashboard concept

┌─────────────────────────────────────────────────────────┐
│ 🤖 EXPLORE-AI                                          │
│ Intelligent Customer Support Operations Center         │
├─────────────────────────────────────────────────────────┤
│ 📩 Total │ ⏳ Pending │ ✅ Approved │ 📤 Sent           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 📧 Gmail → 🤖 AI → 🔍 Analysis → ✍️ Response → 👤 Human│
│                                                         │
├─────────────────────────────────────────────────────────┤
│ 👤 HUMAN APPROVAL CENTER                               │
│                                                         │
│ 🎫 Ticket ID                                            │
│ 👤 Customer                                             │
│ 📦 Order                                                │
│ 🧠 AI Analysis                                          │
│ ✍️ Generated Response                                   │
│                                                         │
│ [💾 Save Draft] [❌ Reject] [✅ Approve]                │
└─────────────────────────────────────────────────────────┘

📊 Google Sheets Ticket Management

Google Sheets is used as the ticket tracking and Human-in-the-Loop state store.

#

Field

Purpose

1

🎫 Ticket ID

Unique ticket identifier

2

📨 Gmail Message ID

Original Gmail message

3

🧵 Gmail Thread ID

Gmail conversation

4

👤 Customer Name

Parsed customer

5

📧 Customer Email

Customer address

6

📝 Subject

Email subject

7

🏷️ Category

Support category

8

🚨 Priority

Ticket priority

9

💬 Customer Issue

Reported issue

10

🧠 Support Analysis

AI analysis

11

✍️ Draft Reply

Generated response

12

🔄 Status

Workflow state

13

🕒 Created At

Creation timestamp

14

👤 Reviewed By

Human reviewer

15

📝 Review Notes

Review comments

16

✅ Approval

Approval state

17

⏱️ Approval Timestamp

Approval time

18

📤 Final Response

Sent response

Ticket lifecycle

⏳ PENDING_REVIEW
        │
        ├── ❌ REJECTED → 🔒 CLOSED
        │
        └── ✅ APPROVED
                │
                ▼
              📤 SENT

📧 Gmail Integration

Gmail API is used for both customer-email retrieval and controlled response delivery.

📥 Gmail Reader

Used to:

Retrieve customer emails

Read message metadata

Parse sender information

Extract subject

Extract email body

Track Gmail message/thread IDs

Avoid repeatedly processing previously handled messages

📤 Gmail Sender

Used only for approved customer responses.

This separation supports safer control of read and send operations.

🔐 Authentication & Security

Google OAuth 2.0 is used for Gmail and Google Sheets access.

Sensitive files must remain local:

.env
credentials.json
token.json
gmail_send_token.json
sheets_token.json

🚨 Never commit credentials, API keys, OAuth tokens, or secrets to GitHub.

🗂️ Project Structure

c-support-Ai-Agent/
│
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📄 .env.example
│
├── 📁 src/
│   ├── 🖥️ app_streamlit.py
│   ├── 🤖 crewai-app.py
│   ├── ⚙️ customer_support_pipeline.py
│   │
│   ├── 📁 agents/
│   │   ├── email_classifier_agent.py
│   │   ├── email_classifier_task.py
│   │   ├── customer_support_agent.py
│   │   ├── customer_support_task.py
│   │   ├── response_generator_agent.py
│   │   └── response_generator_task.py
│   │
│   ├── 📁 services/
│   │   ├── gmail_service.py
│   │   ├── gmail_sender_service.py
│   │   ├── google_sheets_service.py
│   │   ├── approval_service.py
│   │   └── ticket_processor.py
│   │
│   └── 📁 config/
│
└── 🧪 tests/
    ├── conftest.py
    ├── test_project.py
    ├── test_email_response.py
    └── integration/

🧪 Testing

The project includes an automated pytest validation suite.

Run:

pytest .\tests -v

Current validation result

========================
8 passed
0 failed
0 errors
========================

Automated checks

✅ Python environment
✅ Google Sheets service
✅ Gmail service
✅ Gmail sender service
✅ CrewAI agent imports
✅ Ticket processor
✅ Customer response signature
✅ Duplicate signature prevention

Additional integration scripts are maintained for:

📧 Gmail
📊 Google Sheets
🔐 OAuth
👤 Human approval
📤 Ticket processing

⚙️ Installation

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd c-support-Ai-Agent

2. Create virtual environment

Windows:

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

🔑 Environment Configuration

Create .env in the project root.

Example:

GOOGLE_SHEET_ID=your_google_sheet_id

Add any additional LLM/CrewAI environment variables required by your application.

Use .env.example to document required variables without exposing secrets.

▶️ Running the Application

🖥️ Start Streamlit

From the project root:

streamlit run .\src\app_streamlit.py

Open:

http://localhost:8501

🤖 Run CrewAI Pipeline

From src:

python .\crewai-app.py

The pipeline will:

📧 Read the customer email

🏷️ Classify the request

🔍 Analyze the issue

✍️ Generate a response

🧹 Clean the response

✨ Add the official signature

📊 Create the Google Sheets ticket

⏳ Set status to PENDING_REVIEW

No response is automatically sent at this stage.

📤 Process Approved Tickets

After a human approves a ticket:

python -c "from services.ticket_processor import process_approved_tickets; process_approved_tickets()"

The processor:

🔎 Finds approved tickets

📄 Reads the approved response

📤 Sends it through Gmail

📊 Updates Google Sheets

✅ Changes status to SENT

🎬 Recommended Project Demo

For a customer/reviewer demonstration:

1️⃣ Customer sends email

📧 Gmail
    ↓
"Replacement Request"

2️⃣ AI processes the request

🤖 Classifier
      ↓
🔍 Support Analysis
      ↓
✍️ Response Generator

3️⃣ Ticket created

📊 Google Sheets

Status   : PENDING_REVIEW
Approval : PENDING

4️⃣ Human reviews

Open:

🖥️ Streamlit
      ↓
👤 Human Approval Center

5️⃣ Human approves

⏳ PENDING_REVIEW
        ↓
     ✅ APPROVED

6️⃣ Response is sent

📤 Approved Queue
        ↓
     Gmail API
        ↓
📧 Customer receives email

7️⃣ Final state

Approval : APPROVED
Status   : SENT

🛡️ Safety Principles

Explore-AI follows a Human-in-the-Loop AI model.

🤖 AI can

📖 Read

🏷️ Classify

🔍 Analyze

✍️ Draft

💡 Recommend

👤 Human controls

👀 Final review

✏️ Editing

✅ Approval

❌ Rejection

⚙️ System executes

📊 Ticket tracking

📤 Approved-ticket processing

📧 Gmail delivery

🔄 Status updates

This prevents uncontrolled autonomous customer communication.

🚀 Future Enhancements

Potential enhancements include:

🧠 RAG / Knowledge Base integration
😊 Customer sentiment analysis
📦 Product/order database integration
🖼️ Attachment and image analysis
⏱️ SLA monitoring
👥 Role-based reviewer access
📜 Audit logging
📊 Advanced analytics
🗄️ Production database
🐳 Docker deployment
🔄 CI/CD with GitHub Actions
🧪 Automated regression testing
💬 Conversation memory

💼 Business Value

Explore-AI helps customer-support teams:

⚡ Prepare responses faster
📉 Reduce repetitive manual work
🎯 Standardize support communication
🧠 Use AI for issue analysis
👤 Maintain human accountability
📊 Track support tickets centrally
🔐 Control outbound communication
📈 Build an extensible AI-support platform

📌 Project Status

🟢 Functional / Demo Ready

✅ Gmail reading
✅ Customer email parsing
✅ AI classification
✅ Customer support analysis
✅ AI response generation
✅ Response cleanup
✅ Official signature
✅ Google Sheets ticket creation
✅ Human approval workflow
✅ Gmail sending
✅ SENT status tracking
✅ Streamlit dashboard
✅ Automated pytest validation

🧰 Technology Stack

Technology

Role

🐍 Python

Application development

🤖 CrewAI

Multi-agent orchestration

📧 Gmail API

Email integration

📊 Google Sheets API

Ticket management

🖥️ Streamlit

Web dashboard

🔐 OAuth 2.0

Authentication

🧪 pytest

Automated testing

⚙️ python-dotenv

Environment configuration

👨‍💻 Author

Nataraj A

🚀 AI Automation | 🤖 Generative AI | 🧠 CrewAI | 🐍 Python

Explore-AI Customer Support Agent

<p align="center">

⭐ If you find this project useful, consider giving the repository a star!

Built with Python 🐍 · CrewAI 🤖 · Gmail 📧 · Google Sheets 📊 · Streamlit 🖥️ · Human Intelligence 👤
