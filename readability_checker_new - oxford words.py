import streamlit as st
from textstat import textstat
import fitz  # PyMuPDF
import re

# -------------------------------
# Functions
# -------------------------------

@st.cache_data
def load_oxford_3000(pdf_path):
    """
    Load Oxford 3000 words from the provided PDF
    """
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
    """
    Extract unique words from user passage
    """
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return set(text.split())


# -------------------------------
# Load Oxford 3000
# -------------------------------
OXFORD_PDF = "American_Oxford_3000.pdf"  # Make sure this PDF is in the same folder
oxford_words = load_oxford_3000(OXFORD_PDF)

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(
    page_title="Readability & Oxford 3000 Checker",
    layout="centered"
)

st.title("English Passage Readability & Vocabulary Checker")

st.write(
    "This tool analyzes **readability**, estimates **CEFR level**, "
    "and identifies **vocabulary (non-Oxford 3000 words)**."
)

st.subheader("Enter Your English Passage")
text = st.text_area("Paste your passage below:", height=260)

if st.button("Analyze Passage"):
    if not text.strip():
        st.warning("Please enter a passage to analyze.")
    else:
        # -------------------------------
        # Readability Score
        # -------------------------------
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

        # -------------------------------
        # Vocabulary Analysis
        # -------------------------------
        passage_words = extract_words(text)
        non_oxford_words = passage_words - oxford_words

        total_words = len(passage_words)
        advanced_count = len(non_oxford_words)
        advanced_percentage = (advanced_count / total_words) * 100 if total_words else 0

        # -------------------------------
        # Display Results
        # -------------------------------
        st.markdown("## Results")

        st.markdown(f"**Flesch Reading Ease Score:** `{flesch_score:.2f}`")
        st.markdown(
            f"<h4 style='color:{color};'>Difficulty Level: {level}</h4>",
            unsafe_allow_html=True
        )
        st.markdown(f"**Estimated CEFR Level:** `{cefr}`")

        st.markdown("---")

        st.markdown("## 🚨 Vocabulary Analysis (Non-Oxford 3000)")
        st.write(f"**Total Unique Words:** {total_words}")
        st.write(f"**(Non-Oxford) Words:** {advanced_count}")
        st.write(f"**Vocabulary Percentage:** {advanced_percentage:.2f}%")

        with st.expander("View (Non-Oxford) Words Used"):
            st.write(sorted(non_oxford_words))

        # -------------------------------
        # Interpretation Scales
        # -------------------------------
        with st.expander("📊 View Interpretation Scales"):
            st.markdown("### Interpretation Scale (Flesch Reading Ease)")
            st.write("""
| Score Range | Interpretation | Approx. Education Level |
|-------------|----------------|--------------------------|
| 90–100 | Very Easy | 5th grade |
| 80–89 | Easy | 6th grade |
| 70–79 | Fairly Easy | 7th grade |
| 60–69 | Standard | 8th–9th grade |
| 50–59 | Fairly Difficult | 10th–12th grade |
| 30–49 | Difficult | College |
| 0–29 | Very Difficult | College graduate |
            """)

            st.markdown("### CEFR Readability Scale")
            st.write("""
| CEFR Level | Description | Typical Reader |
|------------|-------------|----------------|
| A1 | Beginner | Basic English user |
| A2 | Elementary | Simple communication |
| B1 | Intermediate | Everyday language |
| B2 | Upper-Intermediate | Professional/academic |
| C1 | Advanced | Complex texts |
| C2 | Proficient | Expert-level comprehension |
            """)

