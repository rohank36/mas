from openai import OpenAI
import os
import uuid
from jinja2 import Template
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def uid_hash():
    return uuid.uuid4().hex  # 32-character hexadecimal string

def get_datetime()->str:
    return str(datetime.today())

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
        tools =  [{
            "type": "web_search_preview",
            "search_context_size": "high" # amount of context space to use for the search. low, medium, high. 
        }],
        tool_choice = "auto", 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,0.25,2.00)
    health = res.usage.input_tokens / 400000
    return res.output_text,cost,health

def llm_call_main(messages):
    res = client.responses.create(
        model = "gpt-5",
        reasoning = {"effort": "high"},
        text = {"verbosity":"low"}, 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,1.25,10.00)
    health = res.usage.input_tokens / 400000
    return res.output_text,cost,health

def llm_call_nano(messages):
    res = client.responses.create(
        model = "gpt-5-nano",
        text = {"verbosity":"medium"}, 
        input = messages
    )
    cost = calculate_cost(res.usage.input_tokens,res.usage.output_tokens,0.05,0.40)
    health = res.usage.input_tokens / 400000
    return res.output_text,cost,health

def get_worker_system_prompt():
    filepath = "/system_prompts/worker_prompt.md"
    with open(filepath,encoding="utf-8") as f:
        raw_md = f.read()
    template = Template(raw_md)
    worker_prompt = template.render(current_date=get_datetime())
    return worker_prompt

class WorkerAgent:
    """ Core Function: Get information """
    def __init__(self,task,max_steps=20):
        self.uid = uid_hash()
        self.task = task
        self.cost = 0.0
        self.health = 0.0
        self.should_terminate = False
        self.system_prompt = get_worker_system_prompt()
        self.messages = [
            {"role":"system","content":self.system_prompt},
            {"role":"user","content":self.task}
        ]
        self.trajectory = [] # list of search answers to track semantic trajectory of agent.
        self.max_steps = max_steps
    
    def run(self):
        # TODO: have to decide what you want to return.
        for step in range(self.max_steps):

            if step == self.max_steps - 1 or self.health > 0.6 or self.should_terminate:
                final_answer = self.terminate()
                print(f"Agent {self.uid} terminated....")
                return final_answer,self
            
            res,cost,health = llm_call_mini(self.messages)
            self.update_cost_and_health(cost,health)
            self.messages.append({"role":"assistant","content":res})
            
            # do the verifier here?
            # TODO: how to know when done?
            time.sleep(5)
            
    def update_cost_and_health(self,new_cost,health):
        self.cost += new_cost
        self.health = health

    def terminate(self) -> str:
        self.messages += [
            {"role":"user","content":"You have run out of time. Based on your research, give your final answer:\n"}
        ]
        res,cost,health = llm_call_mini(self.messages)
        self.update_cost_and_health(cost,health)
        return res

class VerifierAgent():
    """ Core function: """
    def __init__(self):
        self.uid = uid_hash()
        self.cost = 0.0
        self.health = 0.0
        """
        self.system_prompt = setup_system_prompts()
        self.messages = [
            {"role":"system","content":self.system_prompt},
            {"role":"user","content":self.task}
        ]
        """
    
    def verify(self,agent_messages):
        pass



def system_run():

    raise NotImplementedError


#strong reasoning model as the verifier
#cheaper model to do the work

"""
why do we still need an engineering effort once we have an agi model? 

you'll still need a harness (that scales) so that many agi models can run in parallel and work together to achieve a common goal.
"""

