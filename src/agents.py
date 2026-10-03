from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from src.config import settings
from src.state import TeamState


def get_llm():
    return ChatGroq(
        model=settings.groq_chat_model,
        temperature=0,
        api_key=settings.groq_api_key,
    )


def researcher(state: TeamState) -> dict:
    """Collect facts for the question. Does not write the final answer."""
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a researcher. List short, clear facts for the question. "
                    "Do not invent numbers, names, or sources. "
                    "If you are not sure, write 'Not sure'."
                )
            ),
            HumanMessage(content=state["question"]),
        ]
    )
    return {"research_notes": response.content}


def writer(state: TeamState) -> dict:
    """Write a short answer using only the research notes."""
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a writer. Write a short answer using only the research notes. "
                    "Do not add new facts. If the notes say 'Not sure', say that."
                )
            ),
            HumanMessage(
                content=(
                    f"Question: {state['question']}\n\n"
                    f"Research notes:\n{state['research_notes']}"
                )
            ),
        ]
    )
    return {"draft": response.content}


def critic(state: TeamState) -> dict:
    """Check the draft against the research notes."""
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a critic. Compare the draft to the research notes. "
                    "List problems only: invented facts, missing caveats, or unclear wording. "
                    "If the draft is fine, write 'No issues'."
                )
            ),
            HumanMessage(
                content=(
                    f"Question: {state['question']}\n\n"
                    f"Research notes:\n{state['research_notes']}\n\n"
                    f"Draft:\n{state['draft']}"
                )
            ),
        ]
    )
    return {"critique": response.content}


if __name__ == "__main__":
    notes = researcher({"question": "What is a multi-agent system in one paragraph?"})
    print(notes["research_notes"])