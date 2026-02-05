# Pydantic Output Parser - Structured output with data validation
from pydantic import BaseModel, Field
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os

load_dotenv()

# Define a Pydantic model for structured output
class Person(BaseModel):
    name: str = Field(description="The person's full name")
    age: int = Field(description="The person's age in years")
    city: str = Field(description="The city where the person lives")
    occupation: str = Field(description="The person's job or profession")

# Create PydanticOutputParser with the model
parser = PydanticOutputParser(pydantic_object=Person)

# Initialize the LLM
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    task="text2text-generation",
    temperature=0.7,
    max_new_tokens=200,
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

# Create a prompt template with format instructions
prompt = PromptTemplate(
    template="Extract information about the person from the following text.\n{format_instructions}\n\nText: {text}\n",
    input_variables=["text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

# Create the chain
chain = prompt | llm | parser

# Test with sample input
try:
    result = chain.invoke({
        "text": "John Smith is a 35-year-old software engineer living in San Francisco."
    })
    
    print("Parsed Output:")
    print(f"Name: {result.name}")
    print(f"Age: {result.age}")
    print(f"City: {result.city}")
    print(f"Occupation: {result.occupation}")
    print(f"\nType: {type(result)}")
    
except Exception as e:
    print(f"Error: {e.message}")

