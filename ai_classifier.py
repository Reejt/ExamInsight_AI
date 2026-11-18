
import json
import ollama

# Local Ollama configuration
MODEL_NAME = "llama3.2:1b"

# DBMS topic categories
TOPICS = [
    "Concurrency Control",
    "DBMS Fundamentals",
    "Database Recovery",
    "ER Model",
    "Functional Dependencies",
    "Indexing",
    "Normalization",
    "Relational Algebra",
    "Relational Model",
    "SQL",
    "Transactions"
]


def get_question_text(question):
    """Extract question text from different supported input formats."""
    return (
        question.get("question")
        or question.get("text")
        or question.get("question_text")
        or ""
    )



def classify_batch(questions):
    """Classify questions individually using Ollama."""

    all_results = []

    for index, question in enumerate(questions, start=1):

        question_number = question.get(
            "question_number",
            question.get("question_no", index)
        )

        question_text = get_question_text(question)

        prompt = f"""
You are a DBMS subject expert.

Classify the following ONE examination question.

Allowed topics:
{json.dumps(TOPICS)}

Question:
{question_text}

Return ONLY one JSON object.
Do not return an array.
Do not classify multiple questions.

Use exactly this structure:
{{
  "predicted_topic": "Normalization",
  "confidence": 0.95,
  "explanation": "The question discusses normalization."
}}

The predicted_topic MUST exactly match one of the allowed topics.
Do not return subtopics or concepts as topic names.
For example, Data Independence belongs to DBMS Fundamentals.
"""

        print(f"Analysing question {question_number}...")

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            format="json",
            options={"temperature": 0}
        )

        response_text = response["message"]["content"]
        result = json.loads(response_text)

        # Support either a JSON object or an array response
        if isinstance(result, list):
            if not result:
                raise ValueError("Ollama returned an empty result.")
            result = result[0]

        if "classifications" in result:
            result = result["classifications"][0]

        topic = result.get("predicted_topic", "").strip()

        # Normalize common AI-generated variations
        topic_aliases = {
            "DBMS": "DBMS Fundamentals",
            "Database Management System": "DBMS Fundamentals",
            "Transaction Management": "Transactions",
            "Concurrency": "Concurrency Control",
            "Functional Dependency": "Functional Dependencies",
            "ER Diagram": "ER Model",
            "Relational Database Model": "Relational Model",
            "Database Indexing": "Indexing",
            "Data Independence": "DBMS Fundamentals"
        }

        topic = topic_aliases.get(topic, topic)

        if topic not in TOPICS:
            raise ValueError(
                f"Invalid topic returned for question "
                f"{question_number}: {topic}"
            )



        try:
            confidence = float(result.get("confidence", 0.5))
        except (ValueError, TypeError):
            confidence = 0.5

        all_results.append({
            "question_number": question_number,
            "predicted_topic": topic,
            "confidence": max(0.0, min(1.0, confidence)),
            "explanation": result.get(
                "explanation",
                "Topic identified from question content."
            )
        })

    return all_results



def classify_questions(questions, batch_size=5):
    """
    Classify all questions in batches.

    This function keeps the same interface as the previous Gemini version.
    """

    if not questions:
        return []

    all_results = []
    total_batches = (len(questions) + batch_size - 1) // batch_size

    for start in range(0, len(questions), batch_size):
        batch = questions[start:start + batch_size]
        batch_number = (start // batch_size) + 1

        print(
            f"\nClassifying batch {batch_number}/{total_batches} "
            f"({len(batch)} question(s))..."
        )

        try:
            results = classify_batch(batch)
            all_results.extend(results)
            print("Batch classified successfully.")

        except Exception as error:
            print(f"Classification failed: {error}")
            raise

    return all_results


# Test the local classifier
if __name__ == "__main__":

    test_questions = [
        {
            "question_number": 1,
            "question": "Explain the different normal forms in DBMS."
        },
        {
            "question_number": 2,
            "question": "What is a primary key and a foreign key?"
        },
        {
            "question_number": 3,
            "question": "Explain ACID properties of transactions."
        }
    ]

    print("Testing local Ollama classification...")
    print(f"Model: {MODEL_NAME}")

    try:
        output = classify_questions(test_questions, batch_size=5)

        print("\nCLASSIFICATION RESULTS\n")
        print(json.dumps(output, indent=4))

        print("\nLocal classification completed successfully!")

    except Exception as error:
        print("\nCLASSIFICATION FAILED")
        print(f"Error: {error}")
