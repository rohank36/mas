from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
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

"""
    {
        "type": "web_search_preview",
        "search_context_size": "medium" # amount of context space to use for the search. low, medium, high. 
    }
    """

response = client.responses.create(
    model="gpt-5-mini",
    include = ["web_search_call.action.sources"],
    parallel_tool_calls = True,
    reasoning={"effort": "medium"}, # effort = low, medium, high. "summary":"auto" = auto, concise, detailed
    temperature = 1, # [0,2]. 1 is stable. < 1 samples more likely tokens. > 1 increases probability of sampling lower likelihood next tokens
    text = {"verbosity":"medium"}, # low, medium, high
    tools = tools,
    tool_choice = "auto", # none, auto, required
    
    input="What is the weather in paris right now?",
)

print(response)

