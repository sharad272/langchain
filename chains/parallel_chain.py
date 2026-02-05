from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableParallel  # For parallel execution

load_dotenv()


llm1 = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=0.3
    
)

llm2 = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-20b",
    task="text-generation",
    temperature=0.3
    
)



chat1 = ChatHuggingFace(llm=llm1)
chat2 = ChatHuggingFace(llm=llm2)

prompt1 = PromptTemplate.from_template("Generate short notes on the following topic: {topic}")
prompt2 = PromptTemplate.from_template("Generate a quiz of the following topic: {topic}")

prompt3 = PromptTemplate.from_template("Combine the following notes and quiz: {notes} {quiz}")

parallel_chain = RunnableParallel({
    "notes": prompt1 | chat1,
    "quiz": prompt2 | chat2
}) | prompt3 | chat2

response = parallel_chain.invoke({"topic": "AI"})
print(response)

parallel_chain.get_graph().print_ascii()