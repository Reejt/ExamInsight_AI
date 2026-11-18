
import json
from pathlib import Path


def load_sample_papers():
    folder = Path("data/sample_papers")

    all_questions = []

    for file_path in sorted(folder.glob("*.json")):

        with open(file_path, "r", encoding="utf-8") as file:
            paper = json.load(file)

        for question in paper["questions"]:

            all_questions.append({
                "paper_id": paper["paper_id"],
                "year": paper["year"],
                "question_number": question["question_number"],
                "question_text": question["question_text"],
                "marks": question["marks"],
                "expected_topic": question.get("expected_topic")
            })

    return all_questions


if __name__ == "__main__":

    questions = load_sample_papers()

    print("Total questions loaded:", len(questions))

    for question in questions[:5]:
        print(question)
