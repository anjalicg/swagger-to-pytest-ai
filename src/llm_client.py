import os
import json
from dotenv import load_dotenv

# Import both SDKs
from openai import OpenAI
from google import genai
from google.genai import types

# Load API keys from your .env file
load_dotenv()

# The master prompt that tells the AI exactly what to do
SYSTEM_PROMPT = """
You are an expert QA automation engineer. 
Analyze the provided OpenAPI JSON schema for boundary conditions (e.g., null values, empty strings, missing required fields, out-of-bounds integers).
Output a structured JSON array of test cases. Each object in the array MUST have exactly three keys:
1. "test_name": A short, unique, descriptive string (e.g., "test_post_pet_missing_name").
2. "payload": The JSON payload for the test.
3. "expected_status": The expected HTTP status code integer.

Output ONLY valid JSON. Do not include markdown formatting, backticks, or explanations.
"""

def generate_test_with_openai(schema_dict: dict) -> str:
    """Passes the schema to OpenAI's GPT-4o model."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Convert the Python dictionary back into a formatted JSON string for the prompt
    schema_string = json.dumps(schema_dict, indent=2)
    user_prompt = f"Here is the OpenAPI JSON schema for a single endpoint:\n\n{schema_string}\n\nGenerate the Pytest code."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2 # Low temperature for more deterministic, structured code output
    )
    
    return response.choices[0].message.content


def generate_test_with_gemini(schema_dict: dict) -> str:
    """Passes the schema to Google's Gemini model."""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    schema_string = json.dumps(schema_dict, indent=2)
    user_prompt = f"Here is the OpenAPI JSON schema for a single endpoint:\n\n{schema_string}\n\nGenerate the Pytest code."
    
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.2
        )
    )
    
    return response.text

# --- Quick Test ---
if __name__ == "__main__":
    # A dummy schema just to test the API connection
    test_schema = {
        "summary": "Find pet by ID",
        "parameters": [{"name": "petId", "in": "path", "required": True, "type": "integer"}]
    }
    
    # Uncomment the one you want to test (make sure your .env has the API key!)
    
    # print("Testing OpenAI...")
    # print(generate_test_with_openai(test_schema))
    
    print("Testing Gemini...")
    print(generate_test_with_gemini(test_schema))