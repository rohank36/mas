from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools2 = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Toronto, Canada",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    
]

def llm_call():
    response = client.responses.create(
        model="gpt-5-nano",
        #parallel_tool_calls = True,
        #reasoning={"effort": "high"}, # effort = low, medium, high. "summary":"auto" = auto, concise, detailed
        #temperature = 1.5, # [0,2]. 1 is stable. < 1 samples more likely tokens. > 1 increases probability of sampling lower likelihood next tokens
        text = {"verbosity":"low"}, # low, medium, high
        #tool_choice = "auto", # none, auto, required
        input="hello",

    )
    return response

res = llm_call()
print(res)
print("\n")
print(res.output_text)
print(res.usage.input_tokens)
print(res.usage.output_tokens)
