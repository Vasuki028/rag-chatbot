import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# We'll use Llama 3 which is fast and free on Groq
MODEL = "llama-3.3-70b-versatile"


def build_prompt(question: str, context_chunks: list[str]) -> str:
    """Build a clean prompt with the question and relevant PDF context"""

    context = "\n\n".join([f"Chunk {i+1}:\n{chunk}" for i, chunk in enumerate(context_chunks)])

    prompt = f"""You are a helpful assistant that answers questions based on the provided PDF content.

Use ONLY the context below to answer the question. If the answer is not found in the context, 
say "I couldn't find that information in the uploaded PDF."

---CONTEXT FROM PDF---
{context}
----------------------

Question: {question}

Answer:"""

    return prompt


def get_answer(question: str, context_chunks: list[str]) -> str:
    """Send question + context to Groq and get an answer"""

    print(f"Sending question to Groq: {question}")

    prompt = build_prompt(question, context_chunks)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions strictly based on provided PDF content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,  # Low temperature = more factual, less creative
        max_tokens=1024
    )

    answer = response.choices[0].message.content
    print("Got answer from Groq ✅")

    return answer


def get_answer_streaming(question: str, context_chunks: list[str]):
    """Streaming version — returns answer word by word (feels faster!)"""

    prompt = build_prompt(question, context_chunks)

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions strictly based on provided PDF content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=1024,
        stream=True  # Stream the response
    )

    # Yield each word as it comes in
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta