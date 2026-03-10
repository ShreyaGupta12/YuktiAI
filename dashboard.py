import streamlit as st
import boto3
import json
import pandas as pd
import plotly.graph_objects as go
import re

# -----------------------------
# AWS CONFIG
# -----------------------------
AWS_REGION = "us-east-1"

lambda_client = boto3.client("lambda", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="YuktiAI Pharma Compliance Auditor",
    page_icon="🧪",
    layout="wide"
)

# -----------------------------
# FUNCTIONS
# -----------------------------

def extract_risk_score(text):
    """Extract Risk Score from AI output"""
    match = re.search(r"Risk Score[:\s]*([0-9\.]+)", text)

    if match:
        return float(match.group(1))

    return None


def risk_gauge(score):
    """Generate risk gauge chart"""

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Compliance Risk Score"},
        gauge={
            'axis': {'range': [0, 1]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 0.4], 'color': "green"},
                {'range': [0.4, 0.7], 'color': "orange"},
                {'range': [0.7, 1], 'color': "red"}
            ],
        }
    ))

    return fig


# -----------------------------
# HEADER
# -----------------------------
st.title("🧪 YuktiAI – AI Pharmaceutical Compliance Auditor")

st.markdown(
"""
YuktiAI automatically analyzes **Batch Manufacturing Records (BMR)**  
and detects **GMP compliance violations using AI + regulatory knowledge**.
"""
)

st.divider()

# -----------------------------
# FILE UPLOAD
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload Batch Record JSON",
        type=["json"]
    )

with col2:
    st.info(
        """
        **Supported Fields**

        - batch_id  
        - product  
        - temperature  
        - sterilization  
        - operator
        """
    )

# -----------------------------
# PROCESS FILE
# -----------------------------
if uploaded_file:

    data = json.load(uploaded_file)

    st.subheader("📄 Uploaded Batch Record")
    st.json(data)

    if st.button("🚀 Run AI Compliance Audit"):

        with st.spinner("Running AI Compliance Analysis..."):

            try:

                response = lambda_client.invoke(
                    FunctionName="yuktiai-audit-processor",
                    InvocationType="RequestResponse",
                    Payload=json.dumps(data)
                )

                result = json.loads(response["Payload"].read())

                st.subheader("🤖 AI Compliance Result")

                if "audit_result" in result:

                    try:

                        bedrock_json = json.loads(result["audit_result"])

                        ai_text = bedrock_json["output"]["message"]["content"][0]["text"]

                        # -----------------------------
                        # METRICS PANEL
                        # -----------------------------

                        m1, m2, m3 = st.columns(3)

                        with m1:
                            st.metric("Batch ID", data.get("batch_id","N/A"))

                        with m2:
                            st.metric("Operator", data.get("operator","Unknown"))

                        with m3:
                            st.metric("Status", "Analyzed")

                        st.divider()

                        # -----------------------------
                        # AI TEXT OUTPUT
                        # -----------------------------

                        st.markdown(ai_text)

                        # -----------------------------
                        # RISK GAUGE
                        # -----------------------------

                        risk = extract_risk_score(ai_text)

                        if risk is not None:

                            st.subheader("📈 Compliance Risk Score")

                            fig = risk_gauge(risk)

                            st.plotly_chart(fig, use_container_width=True)

                            if risk > 0.7:
                                st.error("🔴 High Risk Batch")

                            elif risk > 0.4:
                                st.warning("🟠 Medium Risk Batch")

                            else:
                                st.success("🟢 Low Risk Batch")

                    except Exception:
                        st.write(result["audit_result"])

                else:
                    st.write(result)

            except Exception as e:
                st.error(f"❌ Error calling Lambda: {e}")

st.divider()

# -----------------------------
# AUDIT HISTORY
# -----------------------------

st.header("📊 Audit History")

try:

    table = dynamodb.Table("yuktiai-audit-logs")

    response = table.scan()

    items = response.get("Items", [])

    if items:

        df = pd.DataFrame(items)

        if "timestamp" in df.columns:
            df = df.sort_values(by="timestamp", ascending=False)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.caption(f"{len(df)} audit records found")

    else:
        st.info("No audit records yet.")

except Exception as e:
    st.error(f"❌ Error reading DynamoDB: {e}")