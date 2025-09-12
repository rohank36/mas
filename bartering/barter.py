from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()    
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

general_instruction = """
    Time is off the essence, you must get the deal done before time runs out. Once an agreement has been met by you and the other party, output the price sold/bought at in <done> tags like this: <done>PRICE</done>

    DO NOT output the done tags unless an agreement is reached between you and the other party on the price of the good to be sold/bought, no matter how much time is remaining.
"""

seller_sys_prompt = f"""
    You're in a market. You are selling an apple. You're selling price is 2 tokens. You want your asking price to be met but
    you also want to make a sale. You are willing to go no less than 1.5 tokens. You must try and convince the buyer to agree on your price, use whatever strategy necessary.

    {general_instruction}

    The buyer approaches you now.
"""
seller = [
    {"role":"system","content":seller_sys_prompt}
]

buyer_sys_prompt = f"""
    You're in a market. You are buying an apple. You're bidding price is 1 token. You want your bidding price to be met but 
    you also want to buy an apple. You are willing to pay no more than 1.4 tokens. You must try and convince the seller to agree on your price, use whatever strategy necessary.

    {general_instruction}

    You approach the seller now.
"""
buyer = [
    {"role":"system","content":buyer_sys_prompt}
]

def llm_call(messages):
    response = client.responses.create(
        model="gpt-5-mini",
        #parallel_tool_calls = True,
        reasoning={"effort": "high"}, # effort = low, medium, high. "summary":"auto" = auto, concise, detailed
        #temperature = 1.5, # [0,2]. 1 is stable. < 1 samples more likely tokens. > 1 increases probability of sampling lower likelihood next tokens
        text = {"verbosity":"low"}, # low, medium, high
        #tool_choice = "auto", # none, auto, required
        input=messages,

    )
    return response.output_text

max_iter = 15
for i in range(max_iter):
    res = llm_call(buyer)
    
    print(f"Buyer:\n{res}\n")
    buyer.append({"role":"assistant","content":res})
    seller.append({"role":"user","content":res})

    res = llm_call(seller)
    print(f"Seller:\n{res}\n")
    buyer.append({"role":"assistant","content":res})
    seller.append({"role":"assistant","content":res})

    time = f"Time left: {max_iter-i} minutes\n"
    print(time)
    
    try:
        if "<done>" in buyer[-1].get("content", "") or "<done>" in seller[-1].get("content", ""):
            break
    except Exception as e:
        print("ERROR")
        print(buyer)
        print(seller)
    
    buyer.append({"role":"system","content": time})
    seller.append({"role":"system","content": time})

with open("conversation.txt", "w", encoding="utf-8") as f:
    f.write("=== Buyer Conversation ===\n")
    for turn in buyer:
        role, msg = list(turn.items())[0]
        f.write(f"{role.upper()}: {msg}\n\n")

    f.write("=== Seller Conversation ===\n")
    for turn in seller:
        role, msg = list(turn.items())[0]
        f.write(f"{role.upper()}: {msg}\n\n")