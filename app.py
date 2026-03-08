import streamlit as st
import json

from retriever import retrieve_regulation
from reasoning import analyze

st.title("YuktiAI Compliance Investigator")

uploaded = st.file_uploader("Upload Batch Manufacturing Record", type="json")

if uploaded:

    bmr = json.load(uploaded)

    st.subheader("Batch Record")
    st.json(bmr)

    regs = retrieve_regulation(bmr["deviation"])

    severity, reasoning = analyze(bmr, regs)

    if severity == "CRITICAL":
        st.error("🔴 Critical Non-Compliance")
    else:
        st.success("🟢 Minor Incident")

    st.subheader("Reasoning Chain")

    for r in reasoning:
        st.write("-", r)

    st.subheader("Relevant Regulation")

    for r in regs:
        st.write(r)