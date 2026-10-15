from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. prompt template
prompt = ChatPromptTemplate.from_template("Explain {topic} in simple words")

# 2. model
model = ChatOllama(model="llama3.2")

# 3. Output parser
parser = StrOutputParser()

# step-by-step manual flow
# Format the prompt
# formatted_prompt = prompt.format_messages(topic="Machine Learning")

# # Call the model manually
# response = model.invoke(formatted_prompt)

# # Parse the output manually
# final_output = parser.parse(response.content)

# print(final_output)

chain = prompt | model | parser
result = chain.invoke("Machine Learning")
print(result)
