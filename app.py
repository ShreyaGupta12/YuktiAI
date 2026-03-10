import streamlit as st
import json

from retriever import retrieve_regulation
from reasoning import analyze

st.set_page_config(page_title="YuktiAI", page_icon="🧪")

st.title("🧪 YuktiAI – Pharmaceutical Compliance Investigator")

st.write(
    "Upload a Batch Manufacturing Record (JSON) to automatically detect "
    "GMP compliance deviations using AI."
)

uploaded = st.file_uploader("Upload Batch Manufacturing Record", type="json")

if uploaded:

    bmr = json.load(uploaded)

    st.subheader("📄 Batch Manufacturing Record")
    st.json(bmr)

    # ----------------------------
    # Retrieve regulations
    # ----------------------------

    regs = retrieve_regulation(json.dumps(bmr))

    # ----------------------------
    # Run compliance analysis
    # ----------------------------

    severity, reasoning, cited_regs = analyze(bmr, regs)

    st.subheader("🤖 Compliance Result")

    if severity == "CRITICAL":
        st.error("🔴 Critical Non-Compliance Detected")

    elif severity == "MAJOR":
        st.warning("🟠 Major Compliance Issue")

    else:
        st.success("🟢 Minor Incident")

    # ----------------------------
    # Reasoning Chain
    # ----------------------------

    st.subheader("🧠 AI Reasoning Chain")

    for r in reasoning:
        st.write("•", r)

    # ----------------------------
    # Regulations
    # ----------------------------

    st.subheader("📜 Relevant Regulations")

    for r in cited_regs:
        st.write("•", r)
