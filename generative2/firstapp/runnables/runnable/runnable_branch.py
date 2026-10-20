
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableBranch,RunnablePassthrough,RunnableLambda

prompt = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=["topic"]
)

prompt2 = PromptTemplate(
    template="Summarize the following text:\n{text}",
    input_variables=["text"]
)

model = ChatOllama(
    model="llama3.2",
    temperature=0
)

parser = StrOutputParser()

# Step 1: Generate report
report_gen_chain = RunnableSequence(
    prompt,
    model,
    parser
)

# Step 2: Choose whether to summarize
branch_chain = RunnableBranch(
    (
        lambda x: len(x["text"].split()) > 500,
        RunnableSequence(
            prompt2,
            model,
            parser
        )
    ),
    RunnableLambda(lambda x: x["text"])
)

final_chain = RunnableSequence(
    report_gen_chain,
    RunnableLambda(lambda report: {"text": report}),
    branch_chain
)

result = final_chain.invoke({
    "topic": "Russia vs Ukraine"
})

print(result)
