# YuktiAI – AI-Powered Pharmaceutical Compliance Auditor

YuktiAI is an AI-driven system that automatically audits pharmaceutical batch manufacturing records for regulatory compliance.  
The platform analyzes manufacturing records using generative AI to detect violations, generate compliance summaries, and assign risk scores.

The goal of YuktiAI is to reduce manual auditing effort and help pharmaceutical manufacturers maintain regulatory readiness.

---

## Problem

Pharmaceutical manufacturing must comply with strict regulatory standards such as:

- FDA 21 CFR Part 211
- cGMP guidelines
- CDSCO Schedule M

Auditing batch manufacturing records manually is time-consuming and prone to human error. Missing information like sterilization records or operator logs can lead to compliance violations and product safety risks.

---

## Solution

YuktiAI automates compliance auditing using generative AI.

The system analyzes batch manufacturing records and produces:

- Compliance summary
- Detected violations
- Risk score indicating compliance risk

The solution uses serverless AWS infrastructure for scalability and reliability.

---

## Architecture

```
Batch Record Upload
        ↓
Streamlit Dashboard
        ↓
AWS Lambda
        ↓
Amazon Bedrock (AI Compliance Analysis)
        ↓
DynamoDB (Audit Logs)
        ↓
Compliance Results Dashboard
```

---

## Technologies Used

- Python
- Streamlit
- AWS Lambda
- Amazon Bedrock
- Amazon DynamoDB
- Amazon S3
- Boto3 SDK

---

## Key Features

- AI-powered compliance auditing
- Automatic detection of regulatory violations
- Risk scoring for manufacturing batches
- Audit history storage for traceability
- Serverless architecture
- Interactive dashboard interface

---

## Example Input

```json
{
  "batch_id": "batch_001",
  "temperature": "21C",
  "sterilization": "not recorded",
  "operator": "John"
}
```

---

## Example Output

**Compliance Summary**

Batch manufacturing record shows partial compliance.

**Violations**

- Sterilization process not recorded
- Incomplete operator documentation

**Risk Score**

0.8

---

## Project Structure

```
YuktiAI
│
├── dashboard.py
├── lambda_function.py
├── batch_001.json
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2 Configure AWS Credentials

```
python -m awscli configure
```

Enter:

- AWS Access Key
- AWS Secret Key
- Region (e.g., us-east-1)

### 3 Run the Dashboard

```bash
streamlit run dashboard.py
```

Open in browser:

```
http://localhost:8501
```

---

## Demo Workflow

1 Upload a batch manufacturing record JSON file  
2 Click **Run AI Compliance Audit**  
3 AWS Lambda processes the record  
4 Amazon Bedrock generates compliance analysis  
5 Results are stored in DynamoDB  
6 Compliance report is displayed in the dashboard

---

## Future Improvements

- Regulatory document retrieval using RAG
- Compliance report PDF generation
- Multi-record batch analysis
- Integration with manufacturing execution systems

---

## Team

YuktiAI was built as part of an AI innovation project exploring the use of generative AI in pharmaceutical regulatory compliance.

---

## License

This project is for educational and demonstration purposes.
