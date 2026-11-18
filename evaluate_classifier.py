
from data_loader import load_sample_papers
from ai_classifier import classify_questions
from sklearn.metrics import accuracy_score, classification_report

print("Loading sample question papers...")

questions = load_sample_papers()

expected = [q["expected_topic"] for q in questions[:5]]

print(f"Total questions: {len(questions)}")
print("Starting local AI classification...")

predictions = classify_questions(questions[:5], batch_size=1)

predicted = [p["predicted_topic"] for p in predictions]

accuracy = accuracy_score(expected, predicted)

print("\nEVALUATION RESULTS")
print("-------------------")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        expected,
        predicted,
        zero_division=0
    )
)
