from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph

from src.agents import critic, get_llm, researcher, writer
from src.state import TeamState


def revise(state: TeamState) -> dict:
    """Rewrite the draft using the critic notes."""
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are the writer doing a final rewrite. "
                    "Use the research notes and the critic notes. "
                    "Do not add new facts. Return only the final answer."
                )
            ),
            HumanMessage(
                content=(
                    f"Question: {state['question']}\n\n"
                    f"Research notes:\n{state['research_notes']}\n\n"
                    f"Draft:\n{state['draft']}\n\n"
                    f"Critic:\n{state['critique']}"
                )
            ),
        ]
    )
    return {"final_answer": response.content}


def build_graph():
    graph = StateGraph(TeamState)
    graph.add_node("researcher", researcher)
    graph.add_node("writer", writer)
    graph.add_node("critic", critic)
    graph.add_node("revise", revise)

    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "critic")
    graph.add_edge("critic", "revise")
    graph.add_edge("revise", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke(
        {
            "question": "Explain a multi-agent system in 4 short sentences.",
            "research_notes": "",
            "draft": "",
            "critique": "",
            "final_answer": "",
        }
    )
    print("RESEARCH\n", result["research_notes"])
    print("\nDRAFT\n", result["draft"])
    print("\nCRITIC\n", result["critique"])
    print("\nFINAL\n", result["final_answer"])