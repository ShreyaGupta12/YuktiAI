import streamlit as st
import boto3
import json
import pandas as pd

st.set_page_config(page_title="YuktiAI Pharma Compliance Auditor", layout="wide")

st.title("🧪 YuktiAI – Pharmaceutical Compliance Auditor")
st.write("Upload a Batch Manufacturing Record (JSON) to run an AI compliance audit.")

uploaded_file = st.file_uploader("Upload Batch Record JSON", type=["json"])

if uploaded_file:

    data = json.load(uploaded_file)

    st.subheader("📄 Uploaded Batch Record")
    st.json(data)

    if st.button("Run AI Compliance Audit"):

        try:
            lambda_client = boto3.client("lambda", region_name="us-east-1")

            response = lambda_client.invoke(
                FunctionName="yuktiai-audit-processor",
                InvocationType="RequestResponse",
                Payload=json.dumps(data)
            )

            result = json.loads(response["Payload"].read())

            st.subheader("🤖 AI Compliance Result")

            if "audit_result" in result:

                try:
                    # Step 1: convert string to JSON
                    bedrock_json = json.loads(result["audit_result"])

                    # Step 2: extract the AI text
                    ai_text = bedrock_json["output"]["message"]["content"][0]["text"]

                    st.markdown(ai_text)

                except Exception as parse_error:
                    st.write("Could not parse AI response:")
                    st.write(result["audit_result"])

            else:
                st.write(result)

        except Exception as e:
            st.error(f"Error calling Lambda: {e}")

# ------------------------
# Audit History
# ------------------------

st.header("📊 Audit History")

try:
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table("yuktiai-audit-logs")

    response = table.scan()
    items = response.get("Items", [])

    if items:
        df = pd.DataFrame(items)
        st.dataframe(df)
    else:
        st.write("No audit records found.")

except Exception as e:
    st.error(f"Error reading DynamoDB: {e}")
