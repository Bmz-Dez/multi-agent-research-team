from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from src.config import settings
from src.state import TeamState


class CriticEvaluation(BaseModel):
    approved: bool = Field(
        description="True if the draft is factual, supported by research notes, and clear. False if it has invented facts, errors, or missing details."
    )
    feedback: str = Field(
        description="Detailed feedback explaining what needs fixing if not approved, or 'No issues' if approved."
    )


def get_llm():
    return ChatGroq(
        model=settings.groq_chat_model,
        temperature=0,
        api_key=settings.groq_api_key,
    )


def researcher(state: TeamState) -> dict:
    """Uses a web search tool to gather real facts before taking notes."""
    search_tool = DuckDuckGoSearchRun()
    
    # 1. Ask search tool for live facts on the question
    try:
        search_results = search_tool.invoke(state["question"])
    except Exception as e:
        search_results = f"Search failed: {e}"

    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a researcher. Summarize the facts from the provided search results to answer the question. "
                    "List short, clear bullet points. Do not invent numbers, names, or sources. "
                    "If the search results do not contain enough info, clearly state what is missing."
                )
            ),
            HumanMessage(
                content=f"Question: {state['question']}\n\nSearch Results:\n{search_results}"
            ),
        ]
    )
    return {"research_notes": response.content}


def writer(state: TeamState) -> dict:
    """Write or revise a short answer using research notes and critic feedback if present."""
    llm = get_llm()
    feedback = state.get("critique", "")
    revision_count = state.get("revision_count", 0)

    prompt_content = (
        f"Question: {state['question']}\n\n"
        f"Research notes:\n{state['research_notes']}\n"
    )

    if feedback and feedback != "No issues":
        prompt_content += f"\nPrevious critique to fix:\n{feedback}\n"

    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a writer. Write a short, high-quality answer using only the research notes. "
                    "If critique feedback is provided, address all issues directly. "
                    "Do not add facts that are not present in the notes."
                )
            ),
            HumanMessage(content=prompt_content),
        ]
    )
    return {
        "draft": response.content,
        "revision_count": revision_count + 1,
    }


def critic(state: TeamState) -> dict:
    """Check the draft against research notes using structured output."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(CriticEvaluation)

    evaluation: CriticEvaluation = structured_llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a strict technical critic. Compare the draft against the research notes. "
                    "Mark approved=True ONLY if the draft is fully supported by the research notes and has no hallucinations. "
                    "Mark approved=False if there are invented facts, contradictions, or missing critical context, "
                    "and provide clear instructions in feedback on what must be corrected."
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

    return {
        "critique": evaluation.feedback,
        "approved": evaluation.approved,
    }


if __name__ == "__main__":
    print("Testing researcher node with live search...")
    res = researcher({"question": "What is the capital of Poland?"})
    print("\n[Research Notes]:\n", res["research_notes"])