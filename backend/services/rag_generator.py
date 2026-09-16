from rag.retriever import retrieve

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def build_context(results):
    context=""
    for result in results:
        context+=result["text"]
        context+="\n\n"
    return context


def build_rag_prompt(question,context):
    return f"""
You are a career guidance assistant.
Use the retrieved knowledge context as your primary source.
Rules:
1. Do not invent unsupported skills or experience.
2. Do not assume the user knows a technology unless stated.
3. If the retrieved context is insufficient, clearly say so.
4. Give practical career recommendations.
5. Keep the answer structured and concise.
Retrieved Knowledge:
{context}
User Question:
{question}
"""


def generate_rag_answer(question,context):
    prompt=build_rag_prompt(question,context)
    response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    return response.text

def ask_rag(question,index,metadata,chunks,top_k=3):

    question = question.strip()
    if not question:
        return {
            "question": question,
            "answer": "Please enter a career-related question.",
            "retrieved_chunks": []
        }
    results=retrieve(question,
                    index,
                    metadata,
                    chunks,
                    top_k)

    context=build_context(results)

    answer=generate_rag_answer(question,context)

    return{
        "question": question,
        "answer": answer,
        "retrieved_chunks":results
    }



