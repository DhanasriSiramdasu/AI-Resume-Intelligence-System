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
    prompt=f"""
You are a career guidance assistant.
Answer the users question using the knowledge context below.

Rules:
-use the provided context as the main source.
-Do not invent unsupported skills or experience.
-If the context is insufficient ,say so.
-Give practical recommendations.

knowledge context:
{context}

User Question:
{question}
"""
    return prompt


def generate_rag_answer(question,context):
    prompt=build_rag_prompt(question,context)
    response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    return response.text

def ask_rag(question,index,metadata,chunks,top_k=3):

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



