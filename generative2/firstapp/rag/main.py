from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

video_id = "kg-G6n3j-rw"

try:
    api = YouTubeTranscriptApi()
    fetched_transcript = api.fetch(
        video_id,
        languages=["hi"],  #'en'
    )
    transcript = " ".join(chunk.text for chunk in fetched_transcript)
    # print(transcript)

except TranscriptsDisabled:
    print("No Caption available for this video")


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunk = splitter.create_documents([transcript])
print(len(chunk))
# 3. Initialize embedding model
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_documents(
    documents=chunk, embedding=embeddings, collection_name="log_documents"
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

result = retriever.invoke("Is video mein kya bataya gaya hai?")

# for doc in result:
#     print("p===",doc.page_content)

llm = ChatOllama(model="llama3.2", temperature=0)

prompt = PromptTemplate(
    template="""
    You are a helpful assistant.
    Answer ONLY from the provided transcript context.
    If the context is insufficient, just say you don't know.
    
    {context}
    Question: {question}
    """,
    input_variables=["context", "question"],
)

question = "Is video mein kya bataya gaya hai?"

context = "\n\n".join(doc.page_content for doc in result)

chain = prompt | llm

response = chain.invoke({
    "context": context,
    "question": question
})

print(response.content)