from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="conversational-generation",
    temperature=0.3
    
)

chat = ChatHuggingFace(llm=llm)

prompt = PromptTemplate.from_template("What is the capital of {country}?")

chain = prompt | chat

response = chain.invoke({"country": "India"})

print(response)
chain.get_graph().print_ascii()

