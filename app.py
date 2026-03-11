import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px

from backend.transcriber import transcribe_audio
from backend.scoring import analyze_transcript

st.set_page_config(page_title="CallAuditAI", layout="wide")

st.title("📞 CallAuditAI - LLM Call Analysis Dashboard")

uploaded_file = st.file_uploader(
"Upload Call Audio",
type=["mp3","wav","m4a","ogg","flac","mp4","webm","mpeg"]
)

transcript = ""

# AUDIO TRANSCRIPTION
if uploaded_file is not None:

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Audio uploaded successfully")

    transcript = transcribe_audio(file_path)

    st.subheader("Transcript")
    st.write(transcript)


# MANUAL TRANSCRIPT OPTION
st.subheader("Or Paste Call Transcript")

manual_text = st.text_area("Paste transcript here")

if manual_text:
    transcript = manual_text


# ANALYSIS
if transcript:

    st.subheader("Analyzing Call with AI...")

    analysis = analyze_transcript(transcript)

    try:
        data = json.loads(analysis)

        scores = {
        "Satisfaction": data["satisfaction_score"],
        "Agent Efficiency": data["agent_efficiency"],
        "Language Quality": data["language_quality"],
        "Time Efficiency": data["time_efficiency"],
        "Bias Reduction": data["bias_reduction"],
        "Customer Emotion": data["customer_emotion"],
        "Overall Quality": data["overall_quality"]
        }

        df = pd.DataFrame(list(scores.items()), columns=["Metric","Score"])

        col1,col2 = st.columns(2)

        with col1:
            fig = px.bar(df, x="Metric", y="Score", title="Agent Performance Metrics")
            st.plotly_chart(fig)

        with col2:
            fig2 = px.pie(df, names="Metric", values="Score", title="Score Distribution")
            st.plotly_chart(fig2)

        st.metric("F1 Score", data["f1_score"])

        st.subheader("Summary")
        st.write(data["summary"])

    except:
        st.error("LLM did not return valid JSON")
        st.write(analysis)