from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from typing import TypedDict

load_dotenv()

class Review(TypedDict):
    summary: str
    sentiment: str

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=0.3
)

chat = ChatHuggingFace(llm=llm)

structured_chat = chat.with_structured_output(Review)

response = structured_chat.invoke("Who is Lisa Vicari?")
print(response)
print(response["summary"])
print(response["sentiment"])