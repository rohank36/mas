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


def llm_call_nano(prompt):
    res = client.responses.create(
        model = "gpt-5-nano",
        text = {"verbosity":"medium"}, 
        input = prompt
    )
    return res

def llm_call_mini():
    res = client.responses.create(
        model = "gpt-5-mini",
        include = ["web_search_call.action.sources"],
        parallel_tool_calls = True,
        reasoning = {"effort": "medium"},
        text = {"verbosity":"medium"}, 
        tools =  [{
            "type": "web_search_preview",
            "search_context_size": "high" # amount of context space to use for the search. low, medium, high. 
        }],
        tool_choice = "auto", 
        input = "What happened to charlie kirk yesterday?"
    )
    return res



response_obj = """
Response(id='resp_009d4cc1ce46d6130068c5b5ca74d08194b5d713c43ef710b0', created_at=1757787594.0, error=None, incomplete_details=None, instructions=None, metadata={}, model='gpt-5-mini-2025-08-07', object='response', output=[ResponseReasoningItem(id='rs_009d4cc1ce46d6130068c5b5cb98308194b834813f293dc812', summary=[], type='reasoning', content=None, encrypted_content=None, status=None), ResponseFunctionWebSearch(id='ws_009d4cc1ce46d6130068c5b5cf7478819493bc4ea5f3ae5a12', action=ActionSearch(query='Charlie Kirk September 12 2025', type='search', sources=[ActionSearchSource(type='url', url='https://www.theguardian.com/us-news/2025/sep/12/erika-kirk-charlie-kirk'), ActionSearchSource(type='url', url='https://www.politico.com/news/2025/09/12/charlie-kirks-widow-says-turning-point-will-carry-on-after-the-assassination-of-her-husband-00562792'), ActionSearchSource(type='url', url='https://apnews.com/article/d893cc16fb0937d507283c710c551ef0'), ActionSearchSource(type='url', url='https://en.wikipedia.org/wiki/Killing_of_Charlie_Kirk'), ActionSearchSource(type='url', url='https://en.wikipedia.org/wiki/Charlie_Kirk'), ActionSearchSource(type='url', url='https://www.goodmorningamerica.com/news/story/manhunt-charlie-kirks-killer-enters-3rd-day-questions-125504696'), ActionSearchSource(type='url', url='https://www.policemag.com/home/top-story/news/15755304/suspect-arrested-in-charlie-kirk-assassination'), ActionSearchSource(type='url', url='https://www.kpbs.org/news/politics/2025/09/12/the-suspect-in-charlie-kirk-killing-has-been-arrested-heres-what-we-know')]), status='completed', type='web_search_call'), ResponseReasoningItem(id='rs_009d4cc1ce46d6130068c5b5d19c448194ad7a62d430782ca9', summary=[], type='reasoning', content=None, encrypted_content=None, status=None), ResponseFunctionWebSearch(id='ws_009d4cc1ce46d6130068c5b5e6b41c8194879e7bec9d5ad18f', action=ActionSearch(query='Tyler James Robinson arrested Charlie Kirk', type='search', sources=[ActionSearchSource(type='url', url='https://apnews.com/article/d893cc16fb0937d507283c710c551ef0'), ActionSearchSource(type='url', url='https://people.com/tyler-robinson-death-penalty-charlie-kirk-shooting-11809405'), ActionSearchSource(type='url', url='https://www.theguardian.com/us-news/2025/sep/12/suspect-charlie-kirk-shooting'), ActionSearchSource(type='url', url='https://time.com/7316376/charlie-kirk-shooting-shooter-suspect-uvu-investigation/'), ActionSearchSource(type='url', url='https://www.washingtonpost.com/national/2025/09/12/trump-kirk-political-violence/f6f5f834-8fd2-11f0-8260-0712daa5c125_story.html'), ActionSearchSource(type='url', url='https://www.aljazeera.com/news/2025/9/12/charlie-kirk-shooter-identified-as-tyler-robinson-22-what-we-know'), ActionSearchSource(type='url', url='https://www.wsls.com/news/national/2025/09/12/man-arrested-in-charlie-kirks-killing-had-no-known-criminal-history-had-become-more-political/'), ActionSearchSource(type='url', url='https://www.cbsnews.com/news/charlie-kirk-shooting-arrest-tyler-robinson/'), ActionSearchSource(type='url', url='https://www.ksl.com/article/51374329'), ActionSearchSource(type='url', url='https://www.washingtonpost.com/nation/2025/09/12/charlie-kirk-shooting-suspect-utah/'), ActionSearchSource(type='url', url='https://www.ksl.com/article/51374329/man-arrested-in-charlie-kirk-killing-had-recently-become-more-political-police-say'), ActionSearchSource(type='url', url='https://www.upi.com/Top_News/US/2025/09/12/utah-resident-custody-charlie-kirk-shooting/3101757690259/')]), status='completed', type='web_search_call'), ResponseReasoningItem(id='rs_009d4cc1ce46d6130068c5b5e8f620819494574e873c688bab', summary=[], type='reasoning', content=None, encrypted_content=None, status=None), ResponseFunctionWebSearch(id='ws_009d4cc1ce46d6130068c5b5f27f9c8194b925c0c027ee66ed', action=ActionSearch(query='Donald Trump posthumously award Charlie Kirk Presidential Medal of Freedom Sept 11 2025', type='search', sources=[ActionSearchSource(type='url', url='https://www.theguardian.com/us-news/2025/sep/13/charlie-kirk-maga-influence'), ActionSearchSource(type='url', url='https://nypost.com/2025/09/12/us-news/charlie-kirks-widow-erika-addresses-supporters-in-first-public-comments-since-husbands-assassination/'), ActionSearchSource(type='url', url='https://www.reuters.com/world/us/helene-aftermath-scenes-devastation-north-carolina-2024-10-09/'), ActionSearchSource(type='url', url='https://www.cbsnews.com/news/trump-charlie-kirk-presidential-medal-of-freedom/'), ActionSearchSource(type='url', url='https://www.nbcnewyork.com/news/national-international/trump-posthumously-award-presidential-medal-of-freedom-charlie-kirk/6390575/'), ActionSearchSource(type='url', url='https://www.wdtv.com/video/2025/09/11/trump-posthumously-award-presidential-medal-freedom-charlie-kirk/'), ActionSearchSource(type='url', url='https://en.wikipedia.org/wiki/Charlie_Kirk'), ActionSearchSource(type='url', url='https://abc7.com/post/trump-posthumously-award-charlie-kirk-presidential-medal-freedom/17793188/'), ActionSearchSource(type='url', url='https://abc11.com/post/trump-posthumously-award-charlie-kirk-presidential-medal-freedom/17793188/'), ActionSearchSource(type='url', url='https://www.wsfa.com/2025/09/11/trump-posthumously-award-charlie-kirk-presidential-medal-freedom/'), ActionSearchSource(type='url', url='https://en.wikipedia.org/wiki/Timeline_of_the_second_Trump_presidency_%282025_Q3%29'), ActionSearchSource(type='url', url='https://www.wsfa.com/video/2025/09/11/trump-posthumously-award-presidential-medal-freedom-charlie-kirk/')]), status='completed', type='web_search_call'), ResponseReasoningItem(id='rs_009d4cc1ce46d6130068c5b5f53b1c8194a190b2e83b4072f0', summary=[], type='reasoning', content=None, encrypted_content=None, status=None), ResponseOutputMessage(id='msg_009d4cc1ce46d6130068c5b62f00348194ad555ec6118f85c2', content=[ResponseOutputText(annotations=[AnnotationURLCitation(end_index=448, start_index=355, title="Man arrested in Charlie Kirk's killing had no known criminal history, had become 'more political'", type='url_citation', url='https://apnews.com/article/d893cc16fb0937d507283c710c551ef0?utm_source=openai'), AnnotationURLCitation(end_index=860, start_index=705, title='Suspect arrested, identified in shooting of Charlie Kirk, officials say - Good Morning America', type='url_citation', url='https://www.goodmorningamerica.com/news/story/manhunt-charlie-kirks-killer-enters-3rd-day-questions-125504696?utm_source=openai'), AnnotationURLCitation(end_index=1203, start_index=1110, title="Man arrested in Charlie Kirk's killing had no known criminal history, had become 'more political'", type='url_citation', url='https://apnews.com/article/d893cc16fb0937d507283c710c551ef0?utm_source=openai'), AnnotationURLCitation(end_index=1672, start_index=1517, title='Suspect arrested, identified in shooting of Charlie Kirk, officials say - Good Morning America', type='url_citation', url='https://www.goodmorningamerica.com/news/story/manhunt-charlie-kirks-killer-enters-3rd-day-questions-125504696?utm_source=openai'), AnnotationURLCitation(end_index=2139, start_index=2027, title='Tyler Robinson Likely Facing Death Penalty if Convicted of Assassinating Charlie Kirk', type='url_citation', url='https://people.com/tyler-robinson-death-penalty-charlie-kirk-shooting-11809405?utm_source=openai'), AnnotationURLCitation(end_index=2632, start_index=2455, title="Charlie Kirk's widow says Turning Point will carry on after the assassination of her husband", type='url_citation', url='https://www.politico.com/news/2025/09/12/charlie-kirks-widow-says-turning-point-will-carry-on-after-the-assassination-of-her-husband-00562792?utm_source=openai'), AnnotationURLCitation(end_index=3180, start_index=3087, title='Killing of Charlie Kirk', type='url_citation', url='https://en.wikipedia.org/wiki/Killing_of_Charlie_Kirk?utm_source=openai')], text='Do you mean “yesterday” relative to today (Saturday, September 13, 2025)? If so, “yesterday” was Friday, September 12, 2025 — here’s what happened and the current, widely reported facts.\n\nShort answer\n- Yesterday (Sept. 12, 2025) law-enforcement officials announced they had arrested a suspect in the fatal shooting of conservative activist Charlie Kirk. ([apnews.com](https://apnews.com/article/d893cc16fb0937d507283c710c551ef0?utm_source=openai))\n\nWhat happened (quick timeline and key facts)\n- The shooting itself happened two days earlier, on September 10, 2025: Charlie Kirk was shot while speaking at a Turning Point USA event at Utah Valley University in Orem, Utah, and was later pronounced dead. ([goodmorningamerica.com](https://www.goodmorningamerica.com/news/story/manhunt-charlie-kirks-killer-enters-3rd-day-questions-125504696?utm_source=openai))  \n- On September 12, authorities arrested a 22‑year‑old Utah man identified in news reports as Tyler James Robinson in connection with the killing; officials said the arrest followed information from family/friends and a multi‑agency investigation. ([apnews.com](https://apnews.com/article/d893cc16fb0937d507283c710c551ef0?utm_source=openai))  \n- Investigators say they recovered a rifle believed to be the weapon (reported as an older imported Mauser .30‑06 bolt‑action rifle), found casings with engraved messages, and believe the shot was fired from a nearby roof. Those physical findings and social‑media/ messaging evidence helped lead to the arrest. ([goodmorningamerica.com](https://www.goodmorningamerica.com/news/story/manhunt-charlie-kirks-killer-enters-3rd-day-questions-125504696?utm_source=openai))  \n- The suspect is being held without bail and is expected to face serious state charges (reports list aggravated murder, felony discharge of a firearm causing serious bodily injury and obstruction); formal charging and arraignment were reported as forthcoming. News coverage has noted the suspect could potentially face capital exposure under Utah law. ([people.com](https://people.com/tyler-robinson-death-penalty-charlie-kirk-shooting-11809405?utm_source=openai))\n\nAftermath and reactions (also reported yesterday)\n- Kirk’s widow, Erika Kirk, gave public remarks saying Turning Point would continue and urging supporters to carry on the work; political figures reacted strongly, and President Donald Trump said he would posthumously award Kirk the Presidential Medal of Freedom. ([politico.com](https://www.politico.com/news/2025/09/12/charlie-kirks-widow-says-turning-point-will-carry-on-after-the-assassination-of-her-husband-00562792?utm_source=openai))\n\nNotes and caveats\n- This is an active criminal investigation and reporting has been evolving over the last 48–72 hours; law enforcement and prosecutors (and defense counsel, once appointed) will release more documents and specifics (affidavits, formal charging documents, timeline of arrest, etc.) in the coming days. Some early arrests/detentions reported in the immediate aftermath were later clarified or released as investigators narrowed suspects. ([en.wikipedia.org](https://en.wikipedia.org/wiki/Killing_of_Charlie_Kirk?utm_source=openai))\n\nDo you want more detail?\n- I can pull together a concise timeline (videos, press‑conference transcripts, probable‑cause affidavit excerpts), summarize the suspect’s booking/charges as they’re filed, or show multiple news pieces (AP, NYT, Washington Post, BBC, etc.). Or, if you meant a different date by “yesterday,” tell me which date and I’ll check that specifically.', type='output_text', logprobs=[])], role='assistant', status='completed', type='message')], parallel_tool_calls=True, temperature=1.0, tool_choice='auto', tools=[WebSearchPreviewTool(type='web_search_preview', search_context_size='high', user_location=UserLocation(type='approximate', city=None, country='US', region=None, timezone=None))], top_p=1.0, background=False, conversation=None, max_output_tokens=None, max_tool_calls=None, previous_response_id=None, prompt=None, prompt_cache_key=None, reasoning=Reasoning(effort='high', generate_summary=None, summary=None), safety_identifier=None, service_tier='default', status='completed', text=ResponseTextConfig(format=ResponseFormatText(type='text'), verbosity='high'), top_logprobs=0, truncation='disabled', usage=ResponseUsage(input_tokens=44259, input_tokens_details=InputTokensDetails(cac
"""

prompt = f"""
Extract all source urls from the text. Your output tet should only contain a each url separated by a comma and nothing else. Here is an example:

url1,url2,url3,url4,..,urln

Here is the text:
{response_obj}
"""
#res = llm_call_mini()
res = llm_call_nano(prompt)
print(res)
print("\n")
print(res.output_text)
print(res.usage.input_tokens)
print(res.usage.output_tokens)
print("\n")
urls = res.output_text.split(",")
print(urls)