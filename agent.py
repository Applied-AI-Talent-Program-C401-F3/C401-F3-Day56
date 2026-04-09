from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from tools import (
    search_doctors,
    check_availability,
    book_appointment,
)

load_dotenv()


# =========================
# Load system prompt
# =========================
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()


# =========================
# Graph State
# =========================
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# =========================
# LLM + Tools
# =========================
tools_list = [
    search_doctors,
    check_availability,
    book_appointment,
]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

llm_with_tools = llm.bind_tools(tools_list)


# =========================
# Agent Node
# =========================
def agent_node(state: AgentState):
    messages = state["messages"]

    # chỉ thêm system prompt 1 lần đầu
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # Logging để debug tool call
    if getattr(response, "tool_calls", None):
        print("Tool Calls:")
        for tool_call in response.tool_calls:
            print(
                f"  - {tool_call['name']}({tool_call['args']})"
            )
    else:
        print("💬 Direct Response")

    return {"messages": [response]}


# =========================
# Build Graph
# =========================
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)

builder.add_edge("tools", "agent")

graph = builder.compile()


# =========================
# CLI Chat Loop
# =========================
if __name__ == "__main__":
    print("=" * 60)
    print("Vinmec Medical Assistant")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    conversation_history = []

    while True:
        user_input = input("Bạn: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("Tạm biệt!")
            break

        conversation_history.append(HumanMessage(content=user_input))

        # chỉ giữ 10 message gần nhất để tránh context quá dài
        conversation_history = conversation_history[-10:]

        print("⏳ Assistant đang xử lý...")

        result = graph.invoke(
            {
                "messages": conversation_history
            }
        )

        final_message = result["messages"][-1]

        print(f"Vinmec Assistant: {final_message.content}")

        # lưu lại toàn bộ message graph trả về
        # để tool call + tool response vẫn nằm trong history
        conversation_history = [
            msg
            for msg in result["messages"]
            if not isinstance(msg, SystemMessage)
        ]
