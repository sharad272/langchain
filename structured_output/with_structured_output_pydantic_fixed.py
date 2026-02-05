from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
import json

load_dotenv()

class Review(BaseModel):
    summary: str
    sentiment: str

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=0.3
)

chat = ChatHuggingFace(llm=llm)

# Method 1: Use a prompt that requests JSON output
prompt = """Analyze the following query and return a JSON response with this exact structure:
{
    "summary": "brief summary here",
    "sentiment": "positive/negative/neutral"
}

Query: Who is Lisa Vicari?

Return ONLY the JSON, no other text."""

try:
    response = chat.invoke(prompt)
    print(response.content)
    # Extract JSON from response
    response_text = response.content if hasattr(response, 'content') else str(response)
    
    # Find JSON in the response (sometimes models add extra text)
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}') + 1
    
    if start_idx != -1 and end_idx > start_idx:
        json_str = response_text[start_idx:end_idx]
        data = json.loads(json_str)
        
        # Now validate with Pydantic
        review = Review(**data)
        
        print("✓ Success with Pydantic validation!")
        print(f"Review object: {review}")
        print(f"Summary: {review.summary}")
        print(f"Sentiment: {review.sentiment}")
    else:
        print("Could not find valid JSON in response")
        print(f"Raw response: {response_text}")
        
except ValidationError as e:
    print(f"Pydantic validation error: {e}")
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
    print(f"Raw response: {response_text}")
except Exception as e:
    print(f"Error: {e}")
