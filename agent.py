from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_doctors, check_availability, book_appointment
from dotenv import load_dotenv

load_dotenv()

# 1. Load System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Define State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Initialize LLM and Tools
tools_list = [search_doctors, check_availability, book_appointment]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"🔧 Calling tool: {tc['name']}({tc['args']})")
    else:
        print(f"💬 Direct response")

    return {"messages": [response]}

# 5. Build Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Define edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat Loop
if __name__ == "__main__":
    print("=" * 60)
    print("Vinmec Medical Assistant – Trợ lý Y tế Thông minh")
    print("    Gõ 'quit' để thoát")
    print("=" * 60)

    conversation_history = []

    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        conversation_history.append(("human", user_input))
        conversation_history = conversation_history[-10:]  # Keep last 10 messages for context
        print("\nVinmec Assistant đang xử lý...")
        result = graph.invoke({"messages": conversation_history})

        final = result["messages"][-1]
        print(f"\nVinmec Assistant: {final.content}")

        conversation_history = result["messages"] 