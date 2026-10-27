"""Streamlit UI:  streamlit run app.py"""
import pandas as pd
import streamlit as st
from resume_parser import extract_text, parse_resume
from matcher import match_jobs, job_from_text

st.set_page_config(page_title="Resume Parser & Job Matcher", page_icon="📄", layout="wide")
st.title("📄 Automated Resume Parser & Job Matching System")
st.caption("NLP-based: text extraction → entity/skill extraction → TF-IDF + skill-overlap matching")

jobs = pd.read_csv("jobs.csv")

with st.sidebar:
    st.header("Settings")
    w_skill = st.slider("Weight: skill match", 0.0, 1.0, 0.6, 0.1)
    st.write(f"Weight: text similarity = **{round(1 - w_skill, 1)}**")
    top_n = st.number_input("Show top N jobs", 1, len(jobs) + 1, 5)
    st.divider()
    st.subheader("Optional: your own job description")
    custom_title = st.text_input("Job title")
    custom_jd = st.text_area("Paste job description", height=150)

file = st.file_uploader("Upload resume (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])

if file:
    text = extract_text(file.read(), file.name)
    if len(text.strip()) < 30:
        st.error("Could not read text from this file (maybe a scanned image PDF). Try another file.")
        st.stop()

    info = parse_resume(text)
    st.subheader("1️⃣ Parsed Resume Details")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Name", info["name"])
    c2.metric("Email", info["email"])
    c3.metric("Phone", info["phone"])
    c4.metric("Experience (yrs)", info["experience_years"])
    st.write("**Education:**", ", ".join(info["education"]))
    st.write("**Skills detected:**", ", ".join(info["skills"]) or "None")

    all_jobs = pd.concat([job_from_text(custom_title, custom_jd), jobs], ignore_index=True) if custom_jd.strip() else jobs
    result = match_jobs(text, set(info["skills"]), all_jobs, w_text=1 - w_skill, w_skill=w_skill).head(int(top_n))

    st.subheader("2️⃣ Best Matching Jobs")
    st.dataframe(result, use_container_width=True, hide_index=True)
    st.bar_chart(result.set_index("Job Title")["Match %"])

    best = result.iloc[0]
    st.subheader("3️⃣ Recommendation")
    st.success(f"Best match: **{best['Job Title']}** at {best['Company']} — {best['Match %']}%")
    if best["Missing Skills"] != "-":
        st.info(f"Skills to learn for this role: {best['Missing Skills']}")

    with st.expander("Show raw extracted text"):
        st.text(text)
else:
    st.info("👆 Upload a resume to start. You can use `sample_resume.txt` from this folder for a quick demo.")
