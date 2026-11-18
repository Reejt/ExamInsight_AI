import ollama

response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": "Explain DBMS normalization in simple terms."
        }
    ]
)

print("\nOLLAMA RESPONSE:\n")
print(response["message"]["content"])
