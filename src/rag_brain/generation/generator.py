from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from rag_brain.config import GROQ_API_KEY, LLM_MODEL

PROMPT_TEMPLATE = """
You are a helpful assistant. Use ONLY the context below to answer.
If the answer is not in the context, say:
"I don't know based on the document."

Context:
{context}

Question:
{question}

Answer:
"""

def build_qa_chain(retriever):
    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain