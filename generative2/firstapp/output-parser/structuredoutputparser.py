from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers.structured import (
    StructuredOutputParser,
    ResponseSchema,
)

# 1. Initialize Ollama model
model = ChatOllama(
    model="llama3.2",
    temperature=0
)

# 2. Define response schemas
schema = [
    ResponseSchema(
        name="fact_1",
        description="First fact about the topic"
    ),
    ResponseSchema(
        name="fact_2",
        description="Second fact about the topic"
    ),
    ResponseSchema(
        name="fact_3",
        description="Third fact about the topic"
    ),
]

# 3. Initialize StructuredOutputParser
parser = StructuredOutputParser.from_response_schemas(schema)

# 4. Create prompt template
template = PromptTemplate(
    template=(
        "Give 3 interesting facts about {topic}.\n"
        "Follow the specified output format.\n"
        "{format_instruction}"
    ),
    input_variables=["topic"],
    partial_variables={
        "format_instruction": parser.get_format_instructions()
    },
)

# 5. Create prompt
prompt = template.invoke({"topic": "black holes"})

# 6. Get model response
result = model.invoke(prompt)

print("\nRaw output:")
print(result.content)

# 7. Parse structured output
final_result = parser.parse(result.content)

print("\nStructured output:")
print(final_result)

# print("\nFirst fact:", final_result["fact_1"])
# print("Second fact:", final_result["fact_2"])
# print("Third fact:", final_result["fact_3"])