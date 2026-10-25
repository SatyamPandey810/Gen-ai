from langchain_text_splitters import CharacterTextSplitter

text = """
LangChain is a framework for developing applications
powered by language models. Text splitters help divide
large documents into smaller chunks for processing.
Smaller chunks are useful for building RAG applications.
"""

splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
)

chunks = splitter.split_text(text)

print("Total chunks:", chunks)

# for i, chunk in enumerate(chunks, start=1):
#     print(f"\nChunk {i}:")
#     print(chunk)
#     print("Length:", len(chunk))
