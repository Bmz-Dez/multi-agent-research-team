from langgraph.graph import END, StateGraph

from src.agents import critic, researcher, writer
from src.state import TeamState

MAX_REVISIONS = 2


def finalize(state: TeamState) -> dict:
    """Sets the final approved draft as the final answer."""
    return {"final_answer": state["draft"]}


def should_continue(state: TeamState) -> str:
    """Decides whether to loop back to writer or finish."""
    is_approved = state.get("approved", False)
    revisions = state.get("revision_count", 0)

    # If the critic approved it, finish
    if is_approved:
        return "finalize"

    # If it hit the revision limit, stop looping to avoid runaway API calls
    if revisions >= MAX_REVISIONS:
        return "finalize"

    # Otherwise, loop back to the writer node with the critique feedback
    return "writer"


def build_graph():
    graph = StateGraph(TeamState)

    # 1. Add nodes
    graph.add_node("researcher", researcher)
    graph.add_node("writer", writer)
    graph.add_node("critic", critic)
    graph.add_node("finalize", finalize)

    # 2. Add edges
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "critic")

    # 3. Conditional routing from critic: loop back or finish
    graph.add_conditional_edges(
        "critic",
        should_continue,
        {
            "writer": "writer",
            "finalize": "finalize",
        },
    )

    graph.add_edge("finalize", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    initial_state: TeamState = {
        "question": "What are 3 key facts about the city of Gdansk?",
        "research_notes": "",
        "draft": "",
        "critique": "",
        "final_answer": "",
        "approved": False,
        "revision_count": 0,
    }

    result = app.invoke(initial_state)

    print("\n--- RESEARCH NOTES ---")
    print(result["research_notes"])
    print("\n--- FINAL CRITIQUE FEEDBACK ---")
    print(f"Approved: {result['approved']}")
    print(result["critique"])
    print(f"Total Revisions Run: {result['revision_count']}")
    print("\n--- FINAL ANSWER ---")
    print(result["final_answer"])