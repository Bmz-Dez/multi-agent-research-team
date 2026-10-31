from typing import TypedDict


class TeamState(TypedDict):
    question: str
    research_notes: str
    draft: str
    critique: str
    final_answer: str
    approved: bool
    revision_count: int