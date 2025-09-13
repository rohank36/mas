from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def calculate_cost(input_tokens,output_tokens,input_cost,output_cost):
    onem = 1000000
    input_cost = (input_tokens/onem) * input_cost
    completion_cost = (output_tokens/onem) * output_cost
    return input_cost + completion_cost

def llm_call_mini(messages):
    res = client.responses.create(
        model = "gpt-5-mini",
        include = ["web_search_call.action.sources"],
        parallel_tool_calls = True,
        reasoning = {"effort": "high"},
        text = {"verbosity":"high"}, 
        tools =  {
            "type": "web_search_preview",
            "search_context_size": "high" # amount of context space to use for the search. low, medium, high. 
        },
        tool_choice = "auto", 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,0.25,2.00)
    return res.output_text,cost

def llm_call_main(messages):
    res = client.responses.create(
        model = "gpt-5",
        reasoning = {"effort": "high"},
        text = {"verbosity":"low"}, 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,1.25,10.00)
    return res.output_text,cost

def llm_call_nano(messages):
    res = client.responses.create(
        model = "gpt-5-nano",
        text = {"verbosity":"medium"}, 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,0.05,0.40)
    return res.output_text,cost



#strong reasoning model as the verifier
#cheaper model to do the work

"""
why do we still need an engineering effort once we have an agi model? 

you'll still need a harness (that scales) so that many agi models can run in parallel and work together to achieve a common goal.
"""

