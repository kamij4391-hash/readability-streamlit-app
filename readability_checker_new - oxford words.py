import streamlit as st
from textstat import textstat
import fitz  # PyMuPDF
import re

# -------------------------------------------------
# Functions
# -------------------------------------------------

@st.cache_data
def load_oxford_3000(pdf_path):
    """Load Oxford 3000 words from the provided PDF"""
    doc = fitz.open(pdf_path)
    words = set()

    for page in doc:
        text = page.get_text().lower()
        text = re.sub(r"[^a-z\s]", " ", text)
        for word in text.split():
            if len(word) > 1:
                words.add(word)

    return words


def extract_words(text):
    """Extract unique words from user passage"""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return set(text.split())


# -------------------------------------------------
# Load Oxford 3000
# -------------------------------------------------

OXFORD_PDF = "American_Oxford_3000.pdf"
oxford_words = load_oxford_3000(OXFORD_PDF)

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------

st.set_page_config(
    page_title="Readability & Vocabulary Checker",
    layout="centered"
)

st.title("📘 English Passage Readability & Vocabulary Checker")

st.write(
    "This tool analyzes **text readability**, estimates **CEFR level**, "
    "and identifies **advanced (non-Oxford 3000) vocabulary**."
)

st.subheader("✍️ Enter Your English Passage")
text = st.text_area("Paste your passage below:", height=260)

if st.button("Analyze Passage"):
    if not text.strip():
        st.warning("Please enter a passage to analyze.")
    else:
        # -------------------------------------------------
        # Readability Score
        # -------------------------------------------------

        flesch_score = textstat.flesch_reading_ease(text)

        if flesch_score >= 90:
            level, color = "Very Easy (5th grade)", "green"
            cefr = "A1 (Beginner)"
        elif flesch_score >= 80:
            level, color = "Easy (6th grade)", "lightgreen"
            cefr = "A2 (Elementary)"
        elif flesch_score >= 65:
            level, color = "Fairly Easy (7th–8th grade)", "yellowgreen"
            cefr = "B1 (Intermediate)"
        elif flesch_score >= 50:
            level, color = "Standard (9th–12th grade)", "orange"
            cefr = "B2 (Upper-Intermediate)"
        elif flesch_score >= 30:
            level, color = "Difficult (College)", "tomato"
            cefr = "C1 (Advanced)"
        else:
            level, color = "Very Difficult (Postgraduate)", "red"
            cefr = "C2 (Proficient)"

        # -------------------------------------------------
        # Vocabulary Analysis
        # -------------------------------------------------

        passage_words = extract_words(text)
        non_oxford_words = passage_words - oxford_words

        total_words = len(passage_words)
        advanced_count = len(non_oxford_words)
        advanced_percent = (advanced_count / total_words) * 100 if total_words else 0

        # -------------------------------------------------
        # Display Results
        # -------------------------------------------------

        st.markdown("## 📊 Results")

        st.markdown(f"**Flesch Reading Ease Score:** `{flesch_score:.2f}`")
        st.markdown(
            f"<h4 style='color:{color};'>Difficulty Level: {level}</h4>",
            unsafe_allow_html=True
        )
        st.markdown(f"**Estimated CEFR Level:** `{cefr}`")

        st.markdown("---")

        st.markdown("## 🚨 Advanced Vocabulary Analysis (Non-Oxford 3000)")
        st.write(f"**Total Unique Words:** {total_words}")
        st.write(f"**Advanced / Non-Oxford Words:** {advanced_count}")
        st.write(f"**Advanced Vocabulary Percentage:** {advanced_percent:.2f}%")

        with st.expander("📋 View Advanced (Non-Oxford) Words"):
            st.write(sorted(non_oxford_words))

        st.caption(
            "⚠️ Readability and CEFR levels are **estimates** based on text complexity "
            "and vocabulary usage, not official certification."
        )
