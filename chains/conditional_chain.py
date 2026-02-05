from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from typing import TypedDict
from langchain_core.runnables import RunnableBranch

load_dotenv()

class Sentiment(TypedDict):
    sentiment: str

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=0.3
    
)


chat = ChatHuggingFace(llm=llm)

prompt = PromptTemplate.from_template("Give the sentiment either Positive or Negative only of the following review: {review}")
prompt2 = PromptTemplate.from_template("Write an appropraite message to the customer based on the sentiment: {sentiment}")

chain = prompt | chat 

response = chain.invoke({"review": "Waht a terrible Product this is. Manufacturer should be ashamed of themselves."})

print(response.content)

# Define condition functions for better readability
def is_positive(x):
    """Check if sentiment is positive"""
    return "positive" in x.get("sentiment", "").lower()

def is_negative(x):
    """Check if sentiment is negative"""
    return "negative" in x.get("sentiment", "").lower()

positive_chain = prompt2 | chat
negative_chain = prompt2 | chat

# RunnableBranch evaluates conditions in order and runs the first matching chain
branch_chain = RunnableBranch(
    (is_positive, positive_chain),  # If positive, use positive_chain
    (is_negative, negative_chain),  # If negative, use negative_chain
    positive_chain  # default chain if no condition matches
)

# First get sentiment, then use branch chain
sentiment_chain = chain | (lambda x: {"sentiment": x.content})
full_chain = sentiment_chain | branch_chain

response = full_chain.invoke({"review": "What a terrible Product this is."})

print(response.content)

branch_chain.get_graph().print_ascii()
