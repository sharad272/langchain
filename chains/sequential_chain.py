from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

from simple_chain import prompt

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="conversational-generation",
    temperature=0.3
    
)

chat = ChatHuggingFace(llm=llm)

prompt1 = PromptTemplate.from_template("What is the capital of {country}?")
prompt2 = PromptTemplate.from_template("What is the population of {country}?")

chain = prompt1 | chat | prompt2 | chat

response = chain.invoke({"country": "India"})
print(response)

chain.get_graph().print_ascii()