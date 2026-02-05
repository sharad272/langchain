# Langchain is the Framework for building LLM applications
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=0.3
    
)

chat = ChatHuggingFace(llm=llm)

response = chat.invoke("Who is the president of the United States?")
print(response)