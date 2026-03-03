import time
import random
from traceloop import tracer

def search_web(query: str):
    """Simulate a web search tool."""
    time.sleep(0.3)
    return {
        "results": [f"Result 1 for {query}", f"Result 2 for {query}"],
        "source": "google"
    }

def summarize_agent(context: dict):
    """Simulate an agent summarization process that crashes."""
    time.sleep(0.1)
    # Bug: This requires "context_text" but we pass "results" instead
    if "context_text" not in context:
        raise KeyError("'context_text' missing from summarizer input. The context handoff dropped the parameter.")
    return "This is a good summary."

@tracer.run()
def main_agent(user_query: str):
    print(f"Starting agent run for query: '{user_query}'")
    
    with tracer.step("user_query_received", query=user_query) as step:
        step["outputs"] = {"intent": "information_retrieval"}
    
    with tracer.step("search_web", query=user_query) as step:
        res = search_web(user_query)
        step["outputs"] = res
        
    print("Web search complete. Attempting summarization...")
    
    with tracer.step("summarize_agent", context=res) as step:
        # This will fail
        summary = summarize_agent(context=res)
        step["outputs"] = {"summary": summary}
        
    print("Agent run complete!")

if __name__ == "__main__":
    try:
        main_agent("What is the capital of France?")
    except Exception as e:
        print(f"Agent crashed: {e}")
        print("\n--> Run 'traceloop list' to view the failure.")
