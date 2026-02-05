from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

# Initialize the LLM with explicit API token configuration
llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text2text-generation",
    temperature=0.3,
    max_new_tokens=100
)

# Create a prompt template
prompt1 = PromptTemplate.from_template("Question: What is the capital of {country}?\nAnswer:")

# Create a chain using LCEL (LangChain Expression Language)
# Chain is a sequence of steps that are executed in order
# prompt1 is the input template
# llm is the model
# StrOutputParser is the output parser
# The chain is executed in order, so the output of the previous step is the input of the next step
chain = prompt1 | llm | StrOutputParser()

# Invoke the chain
response = chain.invoke({"country": "India"})
print(response)
