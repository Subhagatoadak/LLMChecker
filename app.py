import streamlit as st
import pandas as pd
import json
from pydantic import BaseModel
from openai import OpenAI

# Sidebar inputs
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
rubric = st.sidebar.text_area(
    "Detection Instructions (System Prompt)",
    placeholder="Enter instructions for the LLM detection agent..."
)

# Main UI
st.title("Teacher-Grader & LLM Checker: OpenAI-based Detection App")
responses_file = st.file_uploader(
    "Upload student responses file (XLSX or CSV)", type=["xlsx", "csv"]
)
questions_file = st.file_uploader(
    "Upload questions file (XLSX or CSV)", type=["xlsx", "csv"]
)

# Initialize OpenAI client
if api_key:
    client = OpenAI(api_key=api_key)

# Pydantic models for parsing
class ScoringEvent(BaseModel):
    llm_score: int

class EvidenceEvent(BaseModel):
    evidence: list[str]

# Helper: multi-agent LLM detection using client.beta.chat.completions.parse
@st.cache_data(show_spinner=False)
def llm_checker(question: str, answer: str, system_prompt: str):
    # Agent 1: Detection
    detect_completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_prompt or
             "You are an expert detector of AI-generated text. Respond with JSON {'llm_score': int between 0-100}."},
            {"role": "user", "content":
             f"Question: {question}\nAnswer: {answer}\n\nAssign a llm_score between 0 and 100 where 100 means definitely LLM-generated and 0 means definitely human-written. Respond ONLY with JSON."}
        ],
        response_format=ScoringEvent,
        temperature=0
    )
    llm_score = detect_completion.choices[0].message.parsed.llm_score

    # Agent 2: Evidence
    evidence_completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content":
             "You are an evidence extraction agent. Respond with JSON {'evidence': [str,...]}."},
            {"role": "user", "content":
             f"Based on the question and answer below, list evidence points justifying the llm_score.\nQuestion: {question}\nAnswer: {answer}"}
        ],
        response_format=EvidenceEvent,
        temperature=0
    )
    evidence = evidence_completion.choices[0].message.parsed.evidence

    return llm_score, evidence

# Process and display when files are uploaded
enabled = api_key and responses_file and questions_file
if enabled:
    # Read responses
    try:
        if responses_file.name.endswith('.csv'):
            responses_df = pd.read_csv(responses_file)
        else:
            responses_df = pd.read_excel(responses_file)
    except Exception as e:
        st.error(f"Error reading responses file: {e}")
        st.stop()

    # Read questions
    try:
        if questions_file.name.endswith('.csv'):
            questions_df = pd.read_csv(questions_file, header=None)
        else:
            questions_df = pd.read_excel(questions_file, header=None)
    except Exception as e:
        st.error(f"Error reading questions file: {e}")
        st.stop()

    questions_list = questions_df.iloc[:, 0].astype(str).tolist()
    name_col = responses_df.columns[0]
    answer_cols = list(responses_df.columns[1:])

    if len(answer_cols) != len(questions_list):
        st.warning("Mismatch: number of answers does not match number of questions.")

    st.subheader("Sample Responses")
    st.dataframe(responses_df.head())
    st.subheader("Questions")
    st.write(questions_list)

    if st.button("Run LLM Checker"):
        results = []
        progress = st.progress(0)
        total = len(responses_df) * len(answer_cols)
        count = 0
        with st.spinner("Detecting LLM-generated answers..."):
            for _, row in responses_df.iterrows():
                student = row[name_col]
                for idx, col in enumerate(answer_cols):
                    ans = str(row[col])
                    q_text = questions_list[idx] if idx < len(questions_list) else f"Question {idx+1}"
                    score, evidence = llm_checker(q_text, ans, rubric)
                    results.append({
                        "name": student,
                        "question": q_text,
                        "llm_score": score,
                        "evidence": evidence
                    })
                    count += 1
                    progress.progress(min(count / total, 1.0))

        # Build dataframe
        df = pd.DataFrame(results)
        st.subheader("Detailed Detection Results")
        for _, r in df.iterrows():
            with st.expander(f"{r['name']} - Q: {r['question']}"):
                st.write(f"**LLM Score:** {r['llm_score']} / 100")
                st.write("**Evidence:**")
                for e in r['evidence']:
                    st.write(f"- {e}")

        st.subheader("Summary Pivot")
        pivot = df.pivot(index='name', columns='question', values='llm_score')
        st.dataframe(pivot)

        csv_detailed = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Detailed CSV", csv_detailed, 'detection_details.csv')
        csv_summary = pivot.reset_index().to_csv(index=False).encode('utf-8')
        st.download_button("Download Summary CSV", csv_summary, 'detection_summary.csv')
else:
    st.info("Please provide API key, responses file, and questions file to proceed.")
