
import json
from pathlib import Path

# Synthetic DBMS examination questions.
# These are practice questions, NOT actual university papers.

papers = {
    2021: [
        ("Explain the three-schema architecture of DBMS.", 5, "DBMS Fundamentals"),
        ("Differentiate between DBMS and file processing systems.", 5, "DBMS Fundamentals"),
        ("Draw an ER diagram for a college management system.", 10, "ER Model"),
        ("Explain primary keys and foreign keys with examples.", 5, "Relational Model"),
        ("Write an SQL query to retrieve students with marks above 75.", 5, "SQL"),
        ("Explain the basic operations of relational algebra.", 5, "Relational Algebra"),
        ("What is functional dependency? Explain with an example.", 5, "Functional Dependencies"),
        ("Explain 1NF, 2NF and 3NF with suitable examples.", 10, "Normalization"),
        ("Explain ACID properties of database transactions.", 5, "Transactions"),
        ("What is an index? Explain primary and secondary indexes.", 5, "Indexing"),
    ],
    2022: [
        ("Explain data independence and its types.", 5, "DBMS Fundamentals"),
        ("Explain entity, attribute and relationship in an ER model.", 5, "ER Model"),
        ("Convert an ER diagram into relational tables.", 10, "ER Model"),
        ("Explain different types of SQL joins with examples.", 10, "SQL"),
        ("Write SQL queries using GROUP BY and HAVING.", 5, "SQL"),
        ("Explain selection and projection in relational algebra.", 5, "Relational Algebra"),
        ("Define functional dependency and explain its properties.", 5, "Functional Dependencies"),
        ("Explain BCNF with an example.", 10, "Normalization"),
        ("Explain the two-phase locking protocol.", 10, "Concurrency Control"),
        ("Describe database recovery using log-based techniques.", 5, "Database Recovery"),
    ],
    2023: [
        ("Explain the advantages and applications of DBMS.", 5, "DBMS Fundamentals"),
        ("Explain weak entities and identifying relationships.", 5, "ER Model"),
        ("Write SQL queries involving nested subqueries.", 10, "SQL"),
        ("Explain relational algebra set operations.", 5, "Relational Algebra"),
        ("Explain lossless decomposition and dependency preservation.", 10, "Normalization"),
        ("Find the candidate keys of a relation using functional dependencies.", 10, "Functional Dependencies"),
        ("Explain transaction states with a diagram.", 5, "Transactions"),
        ("What are deadlocks? Explain deadlock prevention.", 10, "Concurrency Control"),
        ("Explain checkpointing in database recovery.", 5, "Database Recovery"),
        ("Differentiate between clustered and non-clustered indexes.", 5, "Indexing"),
    ],
    2024: [
        ("Explain the architecture of a database management system.", 5, "DBMS Fundamentals"),
        ("Explain specialization and generalization in ER modeling.", 10, "ER Model"),
        ("Write SQL queries using aggregate functions.", 5, "SQL"),
        ("Explain joins and their different types in SQL.", 10, "SQL"),
        ("Explain the closure of functional dependencies.", 10, "Functional Dependencies"),
        ("Normalize a relation up to 3NF.", 10, "Normalization"),
        ("Explain serializability of database schedules.", 10, "Concurrency Control"),
        ("Explain ACID properties with real-world examples.", 5, "Transactions"),
        ("Describe shadow paging in database recovery.", 5, "Database Recovery"),
        ("Explain B-tree and B+ tree indexing.", 10, "Indexing"),
    ],
    2025: [
        ("Differentiate between logical and physical data independence.", 5, "DBMS Fundamentals"),
        ("Design an ER model for an online shopping application.", 10, "ER Model"),
        ("Write SQL queries using UPDATE, DELETE and INSERT.", 5, "SQL"),
        ("Explain relational algebra division operation.", 5, "Relational Algebra"),
        ("Explain partial and transitive dependencies.", 5, "Functional Dependencies"),
        ("Explain 2NF, 3NF and BCNF with examples.", 10, "Normalization"),
        ("Explain conflict serializability with an example.", 10, "Concurrency Control"),
        ("Describe the different states of a transaction.", 5, "Transactions"),
        ("Explain database backup and recovery techniques.", 10, "Database Recovery"),
        ("Compare B-tree indexing and hash indexing.", 10, "Indexing"),
    ]
}

output_dir = Path("data/sample_papers")
output_dir.mkdir(parents=True, exist_ok=True)

for year, questions in papers.items():
    paper = {
        "paper_id": f"DBMS_{year}",
        "subject": "Database Management Systems",
        "course": "B.Tech Computer Engineering",
        "year": year,
        "source": "Synthetic sample data",
        "questions": []
    }

    for number, (text, marks, expected_topic) in enumerate(questions, 1):
        paper["questions"].append({
            "question_number": number,
            "question_text": text,
            "marks": marks,
            # Ground truth for testing only.
            # Do not send this field to the AI classifier.
            "expected_topic": expected_topic
        })

    file_path = output_dir / f"DBMS_{year}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(paper, file, indent=4, ensure_ascii=False)

    print(f"Created: {file_path}")

print("\nSuccessfully generated 5 DBMS sample papers.")
print("Total questions:", sum(len(q) for q in papers.values()))
