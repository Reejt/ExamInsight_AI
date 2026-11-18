
import re


def extract_marks(question_text):
    """
    Extract marks from common question-paper formats.
    """

    patterns = [
        r"\[\s*(\d+)\s*marks?\s*\]",
        r"\(\s*(\d+)\s*marks?\s*\)",
        r"\[\s*(\d+)\s*\]",
        r"\(\s*(\d+)\s*\)",
        r"(\d+)\s*marks?\s*$",
        r"(\d+)\s*M\s*$"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            question_text,
            flags=re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    return None


def clean_question_text(text):
    """
    Remove unnecessary spaces and line breaks.
    """

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_questions(extracted_text):
    """
    Split extracted PDF text into individual questions.

    Supports formats such as:
    Q.1 Explain DBMS.
    Q1: Explain SQL.
    1. Explain normalization.
    2) Explain transactions.
    """

    question_pattern = re.compile(
        r"(?im)^\s*(?:Q(?:uestion)?\.?\s*)?"
        r"(\d{1,2})\s*[\.\):\-]\s+"
    )

    matches = list(question_pattern.finditer(extracted_text))

    if not matches:
        return [{
            "question_number": 1,
            "question_text": clean_question_text(extracted_text),
            "marks": None
        }] if extracted_text.strip() else []

    questions = []

    for index, match in enumerate(matches):

        start = match.end()

        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(extracted_text)
        )

        question_text = clean_question_text(
            extracted_text[start:end]
        )

        marks = extract_marks(question_text)

        # Remove marks notation from the question itself.
        question_text = re.sub(
            r"\s*(?:\[\s*\d+\s*(?:marks?)?\s*\]"
            r"|\(\s*\d+\s*(?:marks?)?\s*\)"
            r"|\d+\s*(?:marks?|M))\s*$",
            "",
            question_text,
            flags=re.IGNORECASE
        ).strip()

        if question_text:
            questions.append({
                "question_number": int(match.group(1)),
                "question_text": question_text,
                "marks": marks
            })

    return questions


if __name__ == "__main__":

    sample_text = """
    Q.1 Explain the three-schema architecture. [5 Marks]

    Q.2 Differentiate between DBMS and file systems. (5)

    Q.3 Explain normalization with suitable examples. 10 Marks

    Q.4 Explain ACID properties of transactions.
    """

    result = parse_questions(sample_text)

    for question in result:
        print(question)
