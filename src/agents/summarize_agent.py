from typing import List, Dict
from langchain_core.messages import SystemMessage, HumanMessage

from src.llms import get_openai_model


# ------------------------------------------------------------------
# 🧭 System Prompt
# ------------------------------------------------------------------

SUMMARIZE_SYSTEM_PROMPT = """
You are a conversation summarizer for a travel assistant.

Your task is to update a running summary based on new conversation messages.

Focus on capturing:
- Travel destinations and locations mentioned
- Travel dates (departure, return, check-in, check-out)
- Number of passengers/guests (adults, children, infants)
- Travel preferences (budget, airline, hotel class, amenities)
- Specific requirements or constraints
- Decisions made or options chosen
- Important context for future interactions

Rules:
1. Keep the summary concise (max 150 words)
2. Prioritize factual travel details over small talk
3. Update or replace outdated information
4. Remove redundant or irrelevant details
5. Use clear, structured format
6. If current summary is empty, create a new one from scratch

Return ONLY the updated summary text, nothing else.
"""


# ------------------------------------------------------------------
# 🤖 LLM
# ------------------------------------------------------------------

llm = get_openai_model()


# ------------------------------------------------------------------
# 📝 Summarize Function
# ------------------------------------------------------------------

def build_summarize_prompt(current_summary: str, new_messages: List[Dict[str, str]]) -> str:
    """
    Build the prompt for the summarize agent.
    
    Args:
        current_summary: Existing summary (can be empty)
        new_messages: List of dicts with 'role' and 'content' keys
        
    Returns:
        Formatted prompt string
    """
    
    # Format the current summary
    if current_summary.strip():
        summary_section = f"CURRENT SUMMARY:\n{current_summary}\n"
    else:
        summary_section = "CURRENT SUMMARY:\n(No summary yet - this is the start of the conversation)\n"
    
    # Format new messages
    messages_section = "NEW MESSAGES:\n"
    for msg in new_messages:
        role = msg["role"].upper()
        content = msg["content"]
        messages_section += f"{role}: {content}\n"
    
    return f"{summary_section}\n{messages_section}\n\nProvide the UPDATED SUMMARY:"


def update_summary(current_summary: str, new_messages: List[Dict[str, str]]) -> str:
    """
    Update the conversation summary with new messages.
    
    Args:
        current_summary: The current summary text (can be empty string)
        new_messages: List of new message dicts with 'role' and 'content'
        
    Returns:
        Updated summary text
    """
    
    # Build the prompt
    user_prompt = build_summarize_prompt(current_summary, new_messages)
    
    # Create messages for LLM
    messages = [
        SystemMessage(content=SUMMARIZE_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt)
    ]
    
    # Get LLM response
    response = llm.invoke(messages)
    
    # Extract and return the summary
    updated_summary = response.content.strip()
    
    return updated_summary
