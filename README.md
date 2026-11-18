
# ExamInsight AI
### Previous Year Question Paper Analyzer

## Project Overview
ExamInsight AI is a Python-based application that analyzes question paper PDFs, extracts questions, classifies them into topics using a locally running LLM, and displays topic-wise question distribution.

## Technologies Used
- Python
- Streamlit
- Ollama
- Llama 3.2 1B
- Pandas
- Plotly

## Features
- Upload question paper PDFs
- Extract questions automatically
- Classify questions by topic using AI
- Display topic-wise question distribution
- Download analysis as CSV

## Installation

1. Install Python.
2. Install Ollama and download the model:

   ollama pull llama3.2:1b

3. Install project dependencies:

   pip install -r requirements.txt

## Run the Application

Start Ollama, then run:

   streamlit run app.py

## Project Structure

- app.py
- ai_classifier.py
- pdf_extractor.py
- question_parser.py
- data_loader.py
- generate_samples.py
- requirements.txt
- screenshots/

## Dataset
The included practice question paper is synthetic sample data created for demonstrating the project. It is not an authentic university previous-year paper.

## Output
The application displays extracted questions, AI-predicted topics, topic counts, and a bar chart.

## Conclusion
ExamInsight AI demonstrates how a local large language model can help organize examination questions and identify topic-wise patterns.
