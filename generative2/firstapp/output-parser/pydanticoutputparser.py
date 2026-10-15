from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 1. Initialize Ollama model
model = ChatOllama(model="llama3.2", temperature=0)


# 2. Define Pydantic model
class Person(BaseModel):
    name: str = Field(description="Name of the fictional person")
    age: int = Field(gt=18, description="Age of the person, greater than 18")
    city: str = Field(description="City where the person lives")


# 3. Initialize PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=Person)

# 4. Create prompt template
template = PromptTemplate(
    template="Generate the name, age and city of a fictional {place} person \n {format_instruction}",
    input_variables=["place"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
)

# 5. Generate prompt
prompt = template.invoke({"place": "indian"})

result = model.invoke(prompt)

# 7. Parse and validate the response
final_result = parser.parse(result.content)

print(final_result)
