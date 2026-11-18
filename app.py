
import streamlit as st
import pandas as pd
import plotly.express as px
import traceback
import re

from pdf_extractor import extract_text_from_pdf
from question_parser import parse_questions
from ai_classifier import classify_questions


# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="ExamInsight AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 ExamInsight AI")
st.subheader("Previous Year Question Paper Analyzer")

st.write(
    "Upload question paper PDFs to extract questions, "
    "classify them by topic using a local AI model, "
    "and visualize topic-wise question distribution."
)


# -------------------- PDF TEXT EXTRACTION --------------------

def get_text_from_result(result):

    if result is None:
        return ""

    if isinstance(result, str):
        return result

    if isinstance(result, bytes):
        return result.decode("utf-8", errors="ignore")

    if isinstance(result, list):
        return "\n".join(
            get_text_from_result(item)
            for item in result
        )

    if isinstance(result, dict):

        for key in [
            "text",
            "full_text",
            "content",
            "extracted_text"
        ]:
            value = result.get(key)

            if isinstance(value, str) and value.strip():
                return value

        for key in [
            "pages",
            "page_text",
            "page_contents"
        ]:
            value = result.get(key)

            if isinstance(value, (list, dict)):
                return get_text_from_result(value)

        return ""

    return str(result)


# -------------------- QUESTION NORMALIZATION --------------------

def normalize_questions(parsed):

    if parsed is None:
        return []

    if isinstance(parsed, str):
        return [
            q.strip()
            for q in parsed.split("\n")
            if q.strip()
        ]

    if isinstance(parsed, dict):

        if "questions" in parsed:
            return normalize_questions(parsed["questions"])

        for key in ["question", "text", "content"]:

            if isinstance(parsed.get(key), str):
                return [parsed[key].strip()]

        return []

    if isinstance(parsed, list):

        questions = []

        for item in parsed:

            if isinstance(item, str):

                if item.strip():
                    questions.append(item.strip())

            elif isinstance(item, dict):

                question_text = (
                    item.get("question")
                    or item.get("text")
                    or item.get("content")
                )

                if question_text:
                    questions.append(str(question_text).strip())

        return questions

    return []


# -------------------- FALLBACK QUESTION PARSER --------------------

def fallback_parse_questions(text):

    pattern = (
        r"(?im)^\s*"
        r"(?:Q(?:uestion)?\s*)?"
        r"\d{1,3}\s*[\.\):\-]\s+"
    )

    matches = list(re.finditer(pattern, text))

    questions = []

    for i, match in enumerate(matches):

        start = match.end()

        end = (
            matches[i + 1].start()
            if i + 1 < len(matches)
            else len(text)
        )

        question = text[start:end].strip()
        question = re.sub(r"\s+", " ", question)

        if len(question) > 10:
            questions.append(question)

    return questions


# -------------------- SIDEBAR --------------------

with st.sidebar:

    st.header("About")

    st.write("**Project:** Previous Year Question Paper Analyzer")
    st.write("**AI model:** Ollama - Llama 3.2 1B")
    st.write("**Tools:** Python, Streamlit, Pandas, Plotly")

    st.divider()

    st.caption("AI-powered topic classification of exam questions.")


# -------------------- PDF UPLOAD --------------------

uploaded_files = st.file_uploader(
    "Upload question paper PDFs",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    all_results = []
    extraction_errors = []

    st.info(f"{len(uploaded_files)} PDF file(s) uploaded.")

    with st.spinner("Extracting questions from PDFs..."):

        for pdf in uploaded_files:

            try:

                pdf.seek(0)

                extracted_result = extract_text_from_pdf(pdf)

                extracted_text = get_text_from_result(
                    extracted_result
                )

                if not extracted_text.strip():

                    extraction_errors.append(
                        f"{pdf.name}: No readable text was extracted."
                    )

                    continue

                parsed_result = parse_questions(extracted_text)

                questions = normalize_questions(parsed_result)

                if not questions:
                    questions = fallback_parse_questions(
                        extracted_text
                    )

                if not questions:

                    extraction_errors.append(
                        f"{pdf.name}: No questions were detected."
                    )

                    continue

                for question in questions:

                    all_results.append({
                        "paper_name": pdf.name,
                        "question": question
                    })

            except Exception as error:

                extraction_errors.append(
                    f"{pdf.name}: {str(error)}"
                )

    if extraction_errors:

        with st.expander("PDF extraction warnings"):

            for error in extraction_errors:
                st.warning(error)

    # -------------------- DISPLAY EXTRACTED QUESTIONS --------------------

    if all_results:

        st.success(
            f"Successfully extracted {len(all_results)} question(s)."
        )

        st.subheader("Extracted Questions")

        extracted_df = pd.DataFrame(all_results)

        st.dataframe(
            extracted_df,
            use_container_width=True
        )

        # -------------------- CLASSIFICATION BUTTON --------------------

        if st.button(
            "🤖 Classify Questions",
            type="primary"
        ):

            try:

                # Pass dictionaries to the classifier
                questions_to_classify = [
                    {"question": item["question"]}
                    for item in all_results
                ]

                with st.spinner(
                    "AI is classifying questions using Ollama. "
                    "This may take a few minutes..."
                ):

                    predictions = classify_questions(
                        questions_to_classify,
                        batch_size=1
                    )

                if not predictions:

                    st.error(
                        "The AI model did not return any predictions."
                    )

                elif len(predictions) != len(all_results):

                    st.error(
                        "The number of predictions does not match "
                        "the number of extracted questions."
                    )

                else:

                    result_rows = []

                    for original, prediction in zip(
                        all_results,
                        predictions
                    ):

                        # Handle string predictions
                        if isinstance(prediction, str):

                            prediction = {
                                "predicted_topic": prediction,
                                "confidence": "",
                                "explanation": ""
                            }

                        # Handle dictionary predictions
                        if isinstance(prediction, dict):

                            topic = (
                                prediction.get("predicted_topic")
                                or prediction.get("topic")
                                or "Unclassified"
                            )

                            confidence = prediction.get(
                                "confidence",
                                ""
                            )

                            explanation = prediction.get(
                                "explanation",
                                ""
                            )

                        else:

                            topic = "Unclassified"
                            confidence = ""
                            explanation = ""

                        result_rows.append({

                            "Paper": original["paper_name"],

                            "Question": original["question"],

                            "Predicted Topic": topic,

                            "Confidence": confidence,

                            "Explanation": explanation

                        })

                    df = pd.DataFrame(result_rows)

                    st.session_state["analysis_results"] = df

                    st.success(
                        "Question classification completed!"
                    )

            except Exception as error:

                st.error(
                    f"Classification failed: {error}"
                )

                with st.expander("Technical error details"):
                    st.code(traceback.format_exc())

    else:

        st.warning(
            "No questions were found. "
            "Please upload a text-based question paper PDF."
        )


# -------------------- ANALYSIS DASHBOARD --------------------

if "analysis_results" in st.session_state:

    df = st.session_state["analysis_results"]

    st.divider()

    st.header("📊 Analysis Dashboard")

    total_questions = len(df)

    total_topics = df["Predicted Topic"].nunique()

    total_papers = df["Paper"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Questions", total_questions)
    col2.metric("Topics Identified", total_topics)
    col3.metric("Papers Analyzed", total_papers)

    # -------------------- TOPIC DISTRIBUTION --------------------

    st.subheader("Topic-wise Question Distribution")

    topic_counts = (
        df["Predicted Topic"]
        .value_counts()
        .reset_index()
    )

    topic_counts.columns = [
        "Topic",
        "Number of Questions"
    ]

    fig = px.bar(
        topic_counts,
        x="Topic",
        y="Number of Questions",
        title="Number of Questions per Topic",
        text="Number of Questions"
    )

    fig.update_layout(
        xaxis_title="Topic",
        yaxis_title="Number of Questions",
        xaxis_tickangle=-35
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------- TOPIC SUMMARY --------------------

    st.subheader("Topic Summary")

    st.dataframe(
        topic_counts,
        use_container_width=True
    )

    # -------------------- CLASSIFIED QUESTIONS --------------------

    st.subheader("Classified Questions")

    st.dataframe(
        df,
        use_container_width=True
    )

    # -------------------- CSV DOWNLOAD --------------------

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Analysis as CSV",
        data=csv_data,
        file_name="exam_question_analysis.csv",
        mime="text/csv"
    )

    # -------------------- CLEAR ANALYSIS --------------------

    if st.button("Clear Analysis"):

        del st.session_state["analysis_results"]

        st.rerun()
