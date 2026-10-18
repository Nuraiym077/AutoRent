from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from fastapi import APIRouter, HTTPException
from mysite.database.schema import ChatSchema, ResponseSchema

chain_router = APIRouter()

loader = TextLoader("AutoRent.txt", encoding="utf-8")
documents = loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20)

chunks = text_splitter.split_documents(documents)


embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


model = ChatOllama(
    model="llama3.2:latest",
    temperature=0
)

vector_store = InMemoryVectorStore.from_documents(chunks, embeddings)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     """Ты AI-помощник AutoRent.
Отвечай только на русском языке.
Перед ответом изучи предоставленный контекст из базы знаний
и документов AutoRent.

Правила:
- Отвечай только на основе предоставленного контекста.
- Не придумывай информацию, цены и условия аренды.
- Если ответа нет в документах, напиши:
  "Извините, я не нашёл информацию по этому вопросу в базе знаний AutoRent."
- Не используй внешние источники и собственные предположения.
- Отвечай кратко, понятно и вежливо.

Контекст из документов:
{context}
"""),
    ("human", "{question}")
])

structured_model = model.with_structured_output(ResponseSchema)


chain = prompt | model | StrOutputParser() | structured_model

@chain_router.post("/chat")
async def chat(questions: ChatSchema):
    data = questions.question.strip()

    if not data:
        raise HTTPException(status_code=400, detail="Маалымат жок")

    new_document = vector_store.similarity_search(data, k=1)

    response = chain.invoke({"question": data, "context": new_document})
    return {"answer": response}





