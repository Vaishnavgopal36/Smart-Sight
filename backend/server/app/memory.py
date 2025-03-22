# backend/server/app/memory.py
from collections import defaultdict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from settings import GEMINI_API_KEY
import os
import json

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
# Session memory to store query history per session
session_memory = defaultdict(list)
# Query Gemini AI
def query_gemini(user_query, image_descriptions, session_id):
    # Initialize session memory if not present
    if session_id not in session_memory:
        session_memory[session_id] = []

    # Append the new interaction (query + relevant image captions)
    session_memory[session_id].append((user_query, image_descriptions))

    # Weighted Memory Retention Logic
    important_keywords = [
        "cost", "price", "budget", "expense", "afford", "cheap", "expensive", "worth", "fees", "ticket", "spending",
        "history", "historical", "origin", "ancient", "significance", "important", "legacy", "past", "cultural", "tradition", "background",
        "compare", "comparison", "better", "worse", "ranking", "difference", "alternative", "versus", "vs", "best", "top", "popular",
        "distance", "nearby", "location", "how to reach", "route", "transport", "airport", "train", "bus", "directions", "accommodation", "stay", "hotel",
        "experience", "review", "recommend", "suggest", "feedback", "rating", "worth it", "pros", "cons", "should I",
        "available", "open", "timing", "schedule", "closed", "holiday", "hours", "entry",
        "safe", "danger", "risk", "precaution", "rules", "regulations", "prohibited", "allowed", "restricted", "security"
    ]
    
    is_important_query = any(word in user_query.lower() for word in important_keywords)
    print(f"Is important query: {is_important_query}")

    # Retain more memory if the query is important
    memory_limit = 8 if is_important_query else 1  # Adjustable weights
    session_memory[session_id] = session_memory[session_id][-memory_limit:]

    # Create a structured context using past interactions
    full_context = "\n".join(
        f"User: {q}\nAI: {', '.join(resp) if resp else 'No response'}" for q, resp in session_memory[session_id]
    )

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    # Different prompt if image descriptions are missing
    if not image_descriptions:
        input_text = (
            f"### User Query: \n{user_query}\n\n"
            "### Instructions: \n"
            "- If you can correctly answer the user's query without additional details, provide a structured and concise response.\n"
            "- If the query lacks necessary information, inform the user that you cannot answer and ask them to provide more details.\n"
            "- Ensure your response is clear and helpful.\n\n"
            "### Response Format Example:\n"
            '["Key point 1", "Key point 2", "Key point 3"]\n\n'
            "### JSON Response:"
        )
    else:
        input_text = (
            f"### User Query: \n{user_query}\n\n"
            f"### Relevant Context from Recent Interactions: \n{full_context}\n\n"
            "### Instructions: \n"
            "- Provide a structured and concise response.\n"
            "- Format the response as a JSON array where each point is a separate item.\n"
            "- Highlight key points and relevant details.\n"
            "- Summarize in key points.\n"
            "- Ensure the response is positive, helpful, and constructive.\n"
            "- If information is missing, provide the best possible educated insight rather than saying 'No data available'.\n"
            "- Avoid negative phrasing; instead, suggest alternatives or related insights.\n\n"
            "### Response Format Example:\n"
            '["Key point 1", "Key point 2", "Key point 3", "Key point 4"]\n\n'
            "### JSON Response:"
        )

    response = llm.invoke([HumanMessage(content=input_text)])

    try:
        content = response.content if response else '["No relevant insights available."]'

        # Ensure response is a JSON array
        if content.startswith("{"):  # If LLM returns an object, extract the value
            content_dict = json.loads(content)  # Parse JSON safely
            content = json.dumps([content_dict.get("response", "No relevant insights available.")])  # Convert to array
        
        return content  # Always return a JSON array as a string
    except:
        return '["An error occurred while generating the response."]'



def reset_memory():
    global session_memory
    session_memory.clear()
    print("✅ Session memory reset successfully.")
